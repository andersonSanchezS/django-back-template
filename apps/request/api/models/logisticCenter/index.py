# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class LogisticCenter(BaseModel):
    code         = models.CharField(max_length=10, blank=True, null=True, unique=True,  error_messages={'unique': 'Ya existe un centro logístico con este código'})
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe un centro logístico con este nombre'})

    class Meta:
        db_table            = 'logistic_centers'
        verbose_name        = 'logistic_center'
        verbose_name_plural = 'logistic_centers'


class LogisticCenterLog(BaseLog):
    logisticCenter = models.ForeignKey(LogisticCenter, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'logistic_centers_log'
        verbose_name        = 'logistic_center_log'
        verbose_name_plural = 'logistic_centers_log'

    