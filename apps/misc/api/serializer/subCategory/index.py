# Rest Framework
from rest_framework import serializers
# Models
from apps.misc.models import SubCategory
from django.db import transaction


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"
        extra_kwargs = {
            "description": { "error_messages": { "required": "La descripción es requerida" } },
            "code"       : { "error_messages": { "required": "El código es requerido" } },
            "category"   : { "error_messages": { "required": "La categoría es requerida" } }
        }

    @transaction.atomic
    def create(self, validated_data):

        return SubCategory.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):

        return super().update(instance, validated_data)
