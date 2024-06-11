from rest_framework import serializers

from .models import Alcaldia, UsoConstruccion


class AlcaldiaCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alcaldia
        fields = "id", "name"


class UsoConstruccionCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsoConstruccion
        fields = "id", "name"
