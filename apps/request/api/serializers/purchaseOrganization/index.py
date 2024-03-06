# Rest Framework
from rest_framework import serializers
# Models
from apps.request.models import PurchaseOrganization
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException

class PurchaseOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrganization
        fields = '__all__'
        extra_kwargs = {"description": { "error_messages": { "required": "La descripción es requerida" } } }

    
    @transaction.atomic
    def create(self, validated_data):
        try:
            purchaseOrganization = PurchaseOrganization.objects.create(**validated_data)
            return purchaseOrganization
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
