# Rest Framework
from rest_framework import serializers
# Models
from apps.authentication.models import Role
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } } }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            permissionsData = validated_data.pop('permissions')
            role = Role.objects.create(**validated_data)

            if permissionsData:
                role.permissions.set(permissionsData)

            return role
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            permissionsData = validated_data.pop('permissions')
            if permissionsData:
                instance.permissions.set(permissionsData)
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
