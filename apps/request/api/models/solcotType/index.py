# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class SolcotType(BaseModel):
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe un tipo de solcot con este nombre'})
    days         = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table            = 'solcot_types'
        verbose_name        = 'solcot_type'
        verbose_name_plural = 'solcot_types'


class SolcotTypeLog(BaseLog):
    solcotType = models.ForeignKey(SolcotType, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'solcot_types_log'
        verbose_name        = 'solcot_type_log'
        verbose_name_plural = 'solcot_types_log'

    