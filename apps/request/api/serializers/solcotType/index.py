# Rest Framework
from rest_framework import serializers
# Models
from apps.request.models import SolcotType
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class SolcotTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolcotType
        fields = '__all__'
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } },
                        "days"       : { "error_messages": { "required": "La cantidad de dias es requerida" } } }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            solcotType = SolcotType.objects.create(**validated_data)
            return solcotType
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
