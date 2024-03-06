# Rest Framework
from rest_framework import serializers
# Models
from apps.request.models import Tax
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class TaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tax
        fields = '__all__'
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } },
                        "value"       : { "error_messages": { "required": "El valor es requerido" } } }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            tax = Tax.objects.create(**validated_data)
            return tax
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
