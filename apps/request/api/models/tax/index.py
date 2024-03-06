# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class Tax(BaseModel):
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe un impuesto con este nombre'})
    value        = models.FloatField(blank=False, null=False)
    
    class Meta:
        db_table            = 'taxes'
        verbose_name        = 'tax'
        verbose_name_plural = 'taxes'


class TaxLog(BaseLog):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'taxes_log'
        verbose_name        = 'tax_log'
        verbose_name_plural = 'taxes_log'

    