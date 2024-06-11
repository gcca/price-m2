from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .services import PriceM2Service, ServiceError


@extend_schema(
    summary="Cálculo del precio agregado por m2.",
    description=(
        "Dado un código postal y un tipo de construcción,"
        " se calcula el precio por m2 agregado (promedio, máximo o mínimo)"
        " de la alcaldía Álvaro Obregón del Gobierno de la Ciudad de México."
    ),
    responses={
        200: OpenApiResponse(
            OpenApiTypes.OBJECT,
            description="Precio por m2 agregado",
            examples=[
                OpenApiExample(
                    name="respponse_avg",
                    value={
                        "status": True,
                        "payload": {
                            "type": "avg",
                            "price_unit": 1420,
                            "price_unit_construction": 3120,
                            "elements": 100,
                        },
                    },
                    summary='Ejemplo de salida con la agregación "avg"',
                ),
                OpenApiExample(
                    name="respponse_max",
                    value={
                        "status": True,
                        "payload": {
                            "type": "max",
                            "price_unit": 4520,
                            "price_unit_construction": 5120,
                            "elements": 80,
                        },
                    },
                    summary='Ejemplo de salida con la agregación "max"',
                ),
                OpenApiExample(
                    name="respponse_min",
                    value={
                        "status": True,
                        "payload": {
                            "type": "min",
                            "price_unit": 1250,
                            "price_unit_construction": 2120,
                            "elements": 60,
                        },
                    },
                    summary='Ejemplo de salida con la agregación "min"',
                ),
            ],
        ),
        400: OpenApiResponse(
            OpenApiTypes.OBJECT,
            description="Error durante la evaluación",
            examples=[
                OpenApiExample(
                    name="error_zip_code",
                    summary="Error response on zip_code",
                    value={
                        "status": False,
                        "errors": ["No se halló el código zip solicitado"],
                    },
                ),
                OpenApiExample(
                    name="error_construction_type",
                    summary="Error response on construction_type",
                    value={
                        "status": False,
                        "errors": [
                            "Query-parameter `construction_type` inválido: Uso: '?construction_type={1-7}'",
                        ],
                    },
                ),
            ],
        ),
    },
    parameters=[
        OpenApiParameter(
            name="zip_code",
            description="Código postal de la alcaldía Álvaro Obregón.",
            required=True,
            type=str,
            pattern="^.{1,10}$",
            location=OpenApiParameter.PATH,
            examples=[
                OpenApiExample(
                    name="En el predio Colinas del Sur", value="1430"
                ),
                OpenApiExample(name="En el predio Tecolalco", value="1250"),
            ],
        ),
        OpenApiParameter(
            name="aggregate",
            description="Agregación usada para la evaluación. Debe ser uno de los siguientes valores: avg, max o min.",
            required=True,
            type=str,
            pattern="^avg|max|min$",
            location=OpenApiParameter.PATH,
            examples=[
                OpenApiExample(name="Promedio ", value="avg"),
                OpenApiExample(name="Máximo ", value="max"),
                OpenApiExample(name="Mínimo ", value="min"),
            ],
        ),
        OpenApiParameter(
            name="construction_type",
            description="Tipo de construcción usado para filtrar el catastro. Debe ser un número entero del 1 al 7.",
            required=True,
            type=int,
            pattern="^[1-7]$",
            location=OpenApiParameter.QUERY,
            examples=[
                OpenApiExample(name="Áreas verdes", value="1"),
                OpenApiExample(name="Centro de barrio", value="2"),
                OpenApiExample(name="Equipamiento ", value="3"),
                OpenApiExample(name="Habitacional ", value="4"),
                OpenApiExample(name="Habitacional y comercial", value="5"),
                OpenApiExample(name="Industrial ", value="6"),
                OpenApiExample(name="Sin Zonificación", value="7"),
            ],
        ),
    ],
)
@api_view(["GET"])
def aggregated_price_by_m2(request, zip_code=None, aggregate=None):
    if zip_code is None:
        raise ValidationError("Path-parameter `zip_code` nulo.")

    if aggregate is None:
        raise ValidationError("Path-parameter `aggregate` nulo.")

    try:
        construction_type = int(request.GET.get("construction_type"))
    except (ValueError, TypeError) as error:
        raise ValidationError(
            "Query-parameter `construction_type` inválido: Uso: '?construction_type={1-7}'"
        ) from error

    price_m2_service = PriceM2Service()

    try:
        price_m2_result = price_m2_service.calculate(
            zip_code=zip_code,
            aggregate=aggregate,
            construction_type=construction_type,
        )
    except ServiceError as error:
        raise ValidationError(str(error)) from error

    return Response(
        {
            "status": True,
            "payload": {
                "type": price_m2_result["type"],
                "price_unit": price_m2_result["price_unit"],
                "price_unit_construction": price_m2_result[
                    "price_unit_construction"
                ],
                "elements": price_m2_result["elements"],
            },
        }
    )
