# Rest Framework
from rest_framework import serializers
# Models
from apps.authentication.models import Permission
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } } }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            permission = Permission.objects.create(**validated_data)
            return permission
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
