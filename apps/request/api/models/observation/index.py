# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class Observation(BaseModel):
    description  = models.TextField(blank=False, null=False)
    solcot       = models.ForeignKey('request.solcot', on_delete=models.CASCADE)
    supra_solcot = models.ForeignKey('request.supraSolcot', on_delete=models.CASCADE)
    
    class Meta:
        db_table            = 'observations'
        verbose_name        = 'observation'
        verbose_name_plural = 'observations'


class ObservationLog(BaseLog):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'observations_log'
        verbose_name        = 'observation_log'
        verbose_name_plural = 'observations_log'

    