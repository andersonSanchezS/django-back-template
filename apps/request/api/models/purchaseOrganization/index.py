# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class PurchaseOrganization(BaseModel):
    code         = models.CharField(max_length=10, blank=True, null=True, unique=True,  error_messages={'unique': 'Ya existe una organizacion de compra con este código'})
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe una organizacion de compra con este nombre'})

    class Meta:
        db_table            = 'purchase_organizations'
        verbose_name        = 'purchase_organization'
        verbose_name_plural = 'purchase_organizations'


class PurchaseOrganizationLog(BaseLog):
    purchaseOrganization = models.ForeignKey(PurchaseOrganization, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'purchase_organizations_log'
        verbose_name        = 'purchase_organization_log'
        verbose_name_plural = 'purchase_organizations_log'

    