# Rest Framework
from rest_framework import serializers
# Models
from apps.misc.models import Category
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } } }

    @transaction.atomic
    def create(self, validated_data):

        return Category.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):

        return super().update(instance, validated_data)
