# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class CostCenter(BaseModel):
    code         = models.CharField(max_length=10, blank=True, null=True, unique=True,  error_messages={'unique': 'Ya existe un centro de costo con este código'})
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe un centro de costo con este nombre'})

    class Meta:
        db_table            = 'cost_centers'
        verbose_name        = 'cost_center'
        verbose_name_plural = 'cost_centers'


class CostCenterLog(BaseLog):
    costCenter = models.ForeignKey(CostCenter, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'cost_centers_log'
        verbose_name        = 'cost_center_log'
        verbose_name_plural = 'cost_centers_log'

    