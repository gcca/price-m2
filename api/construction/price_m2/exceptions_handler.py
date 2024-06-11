from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def price_m2_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        data = {"status": False, "errors": exc.detail}

        response.data = data

    return response
