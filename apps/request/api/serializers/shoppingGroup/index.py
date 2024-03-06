# Rest Framework
from rest_framework import serializers
# Models
from apps.request.models import ShoppingGroup
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class ShoppingGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingGroup
        fields = '__all__'
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } },
                        "code"       : { "error_messages": { "max_length": "La longitud maxima del código es de 10 caracteres" } } }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            shoppingGroup = ShoppingGroup.objects.create(**validated_data)
            return shoppingGroup
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
