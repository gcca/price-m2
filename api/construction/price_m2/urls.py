from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from . import api_views, viewsets


def completion_routes():
    router = routers.SimpleRouter()

    router.register(
        "alcaldia", viewsets.AlcaldiaCompletionViewSet, basename="alcaldia"
    )

    router.register(
        "uso_construccion",
        viewsets.UsoConstruccionCompletionViewSet,
        basename="uso_construccion",
    )

    return router.urls


urlpatterns = [
    # TODO: el max_length de `zip_code` se fija a 10 para evitar búsquedas innecesarias
    #       hacia db, dado que los códigos postales suelen tener 5 caracteres.
    # Revisitar para definir el formato de zip_code junto con el equipo de producto.
    re_path(
        r"zip-codes/(?P<zip_code>.{1,10})/aggregate/(?P<aggregate>avg|max|min)",
        api_views.aggregated_price_by_m2,
    ),
    path("completion/", include(completion_routes())),
    # api-doc
    path("doc/schema/download", SpectacularAPIView.as_view(), name="schema"),
    path(
        "doc/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "doc/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
