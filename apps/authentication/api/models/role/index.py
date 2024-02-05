# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel


class Role(BaseModel):
    description    = models.CharField(max_length=255, blank=True, null=True)
    permissions    = models.ManyToManyField('authentication.permission', related_name='roles_clearpermission', blank=True)
        
    class Meta:
        db_table            = 'roles'
        verbose_name        = 'role'
        verbose_name_plural = 'roles'