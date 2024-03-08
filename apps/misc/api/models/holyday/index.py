# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class Holyday(BaseModel):
    year         = models.CharField(max_length=10, blank=False, null=False, unique=False,  error_messages={'unique': 'Ya existe una categoría con este código'})
    month        = models.CharField(max_length=10, blank=False, null=False, unique=False,  error_messages={'unique': 'Ya existe una categoría con este código'})
    day          = models.CharField(max_length=10, blank=False, null=False, unique=False,  error_messages={'unique': 'Ya existe una categoría con este código'})
    description  = models.CharField(max_length=255, blank=False, null=False, unique=False, error_messages={'unique': 'Ya existe una categoría con este nombre'})

    class Meta:
        db_table            = 'holydays'
        verbose_name        = 'holyday'
        verbose_name_plural = 'holydays'


class HolydayLog(BaseLog):
    holyday = models.ForeignKey(Holyday, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'holydays_log'
        verbose_name        = 'holyday_log'
        verbose_name_plural = 'holydays_log'

    