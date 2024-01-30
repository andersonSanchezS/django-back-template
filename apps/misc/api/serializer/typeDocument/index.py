# Rest Framework
from rest_framework import serializers
# Models
from apps.misc.models import TypeDocument
from django.db import transaction


class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDocument
        fields = "__all__"
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } } }

    @transaction.atomic
    def create(self, validated_data):

        return TypeDocument.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):

        return super().update(instance, validated_data)
