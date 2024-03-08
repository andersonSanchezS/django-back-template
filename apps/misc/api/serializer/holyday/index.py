# Rest Framework
from rest_framework import serializers
# Models
from apps.misc.models import Holyday
from django.db import transaction


class HolydaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holyday
        fields = "__all__"
        extra_kwargs = {
            "description": { "error_messages": { "required": "La descripción es requerida" } },
            "day"        : { "error_messages": { "required": "El dia es requerido" }  },
            "month"      : { "error_messages": { "required": "El mes es requerido" } },
            "year"       : { "error_messages": { "required": "El año es requerido" }  }
        }

    @transaction.atomic
    def create(self, validated_data):

        return Holyday.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):

        return super().update(instance, validated_data)
