# Rest Framework
from rest_framework import serializers
# Models
from apps.authentication.models import Menu
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'
        extra_kwargs = {
            "description": { "error_messages": { "required": "La descripción es requerida" } },
             "icon": { "error_messages": { "required": "El icono es requerido" } }
        }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            menu = Menu.objects.create(**validated_data)
            return menu
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
