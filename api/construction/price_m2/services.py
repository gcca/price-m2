import logging

from django.db.models import (
    Avg,
    Count,
    ExpressionWrapper,
    F,
    FloatField,
    Max,
    Min,
)

from .constants import NO_CONSTRUCTION_FOUND_MESSAGE, NO_ZIP_CODE_FOUND_MESSAGE
from .models import CatastroInfo, UsoConstruccion


class ServiceError(Exception):
    """Lanzar esta excepción cuando ocurre un error en la lógica de negocio de un servicio.

    Este tipo de excepción y sus derivados son atrapados por los views para mostrar
    el `message` como parte del payload de error de la API.
    """

    __slots__ = ("message",)

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class PriceM2Service:

    def calculate(self, zip_code: str, aggregate: str, construction_type: int):
        """Evalúa la agregación (avg, max, min) filtrando los `CatastroInfo`s por `zip_code`
        y `construction_type`.

        Aplica las siguientes fórmulas a los campos de CatastroInfo:
            price_unit = superficie_terreno / valor_suelo - subsidio
            price_unit_construction = superficie_construccion / valor_suelo - subsidio

        Lanza la excepción `ServiceError` en los siguientes casos:
            * cuando el zip_code no se encuentra en la db, y
            * cuando el construction_type no se encuentra en la db.

        Retorna un diccionario con el siguiente formato:
            {
                "type": Literal["avg", "max", "min"],
                "price_unit": float,
                "price_unit_construction": float,
                "elements": int,
            }

        Por ejemplo:
        >>> price_m2_service = PriceM2Service()
        >>> result = price_m2_service.calculate(
        ...   zip_code="10101",
        ...   aggregate="avg",
        ...   construction_type=1,
        ... )
        >>> result
        ... {
        ...    "type": "avg",
        ...    "price_unit": 67.11764705882354,
        ...    "price_unit_construction": 29.470588235294116,
        ...    "elements": 2,
        ... }
        """

        if not UsoConstruccion.objects.filter(id=construction_type).exists():
            logging.warning(
                "Error buscando construction_type=%s. Info: zip_code=%s, aggregate=%s",
                construction_type,
                zip_code,
                aggregate,
            )
            raise ServiceError(NO_CONSTRUCTION_FOUND_MESSAGE)

        if not CatastroInfo.objects.filter(codigo_postal=zip_code).exists():
            logging.warning(
                "Error buscando zip_code=%s. Info: aggregate=%s, construction_type=%s",
                zip_code,
                aggregate,
                construction_type,
            )
            raise ServiceError(NO_ZIP_CODE_FOUND_MESSAGE)

        # TODO: confirmar intención de los cálculos para actualizar
        # los tests con cálculos manuales.
        # Considerar posible edge-cases, v.g., valor_suelo cerca a cero (typo),
        # o la limpieza de data.

        price_unit_expression = ExpressionWrapper(
            (F("superficie_terreno") / F("valor_suelo")) - F("subsidio"),
            output_field=FloatField(),
        )

        price_unit_construction_expression = ExpressionWrapper(
            (F("superficie_construccion") / F("valor_suelo")) - F("subsidio"),
            output_field=FloatField(),
        )

        match aggregate:
            case "avg":
                aggregation_operator = Avg
            case "max":
                aggregation_operator = Max
            case "min":
                aggregation_operator = Min
            case _:
                # Este código no debería ejecutarse nunca.
                # Se retorna un `ServiceError` para mostrar un freindly-message
                #   en caso este escenario llegue a producción.
                logging.debug(
                    "Unreachable code: llegó el aggregate '%s' a PriceM2Service.calculate.",
                    aggregate,
                )
                raise ServiceError(
                    f"Aggregate '{aggregate}' no soportado. Valores válidos: avg, max, min."
                )

        catastro_info_result = CatastroInfo.objects.filter(
            codigo_postal=zip_code, uso_construccion=construction_type
        ).aggregate(
            price_unit=aggregation_operator(price_unit_expression),
            price_unit_construction=aggregation_operator(
                price_unit_construction_expression
            ),
            elements=Count("*"),
        )

        # TODO: ¿Es necesario un PriceM2Result como wrapper de los resultados en lugar de dict?
        return {
            "type": aggregate,
            "price_unit": catastro_info_result["price_unit"],
            "price_unit_construction": catastro_info_result[
                "price_unit_construction"
            ],
            "elements": catastro_info_result["elements"],
        }
