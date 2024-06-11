import logging

from rest_framework import viewsets

from .constants import (
    ALCALDIA_ACTUAL_LIMIT,
    ALCALDIA_LIMIT_WARNING,
    USO_CONSTRUCCION_ACTUAL_LIMIT,
    USO_CONSTRUCCION_LIMIT_WARNING,
)
from .models import Alcaldia, UsoConstruccion
from .serializers import (
    AlcaldiaCompletionSerializer,
    UsoConstruccionCompletionSerializer,
)


class AlcaldiaCompletionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlcaldiaCompletionSerializer

    def get_queryset(self):
        alcaldias = Alcaldia.objects.all().only("id", "name")[
            :ALCALDIA_ACTUAL_LIMIT
        ]

        if len(alcaldias) >= ALCALDIA_LIMIT_WARNING:
            logging.warning(
                "Se está superando el límite de elementos para retornar Alcaldia: valor_actual=%s, warning_limit=%s",
                len(alcaldias),
                ALCALDIA_LIMIT_WARNING,
            )

        return alcaldias


class UsoConstruccionCompletionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UsoConstruccionCompletionSerializer

    def get_queryset(self):
        usos = UsoConstruccion.objects.all().only("id", "name")[
            :USO_CONSTRUCCION_ACTUAL_LIMIT
        ]

        if len(usos) >= USO_CONSTRUCCION_LIMIT_WARNING:
            logging.warning(
                "Se está superando el límite de elementos para retornar UsoConstruccion: valor_actual=%s, warning_limit=%s",
                len(usos),
                USO_CONSTRUCCION_LIMIT_WARNING,
            )

        return usos
