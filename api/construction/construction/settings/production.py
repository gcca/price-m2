from os import environ

from .base import *

DEBUG = False

ALLOWED_HOSTS = [environ["PRICE_M2_DOMAIN"]]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ["PRICE_M2_DB_NAME"],
        "USER": environ["PRICE_M2_DB_USER"],
        "PASSWORD": environ["PRICE_M2_DB_PASSWORD"],
        "HOST": environ["PRICE_M2_DB_HOST"],
        "PORT": environ["PRICE_M2_DB_PORT"],
    }
}
