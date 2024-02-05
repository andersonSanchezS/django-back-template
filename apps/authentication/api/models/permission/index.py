# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel


class Permission(BaseModel):

    description        = models.CharField(max_length=255, blank=True, null=True)
        
    class Meta:
        db_table            = 'permissions'
        verbose_name        = 'permission'
        verbose_name_plural = 'permissions'