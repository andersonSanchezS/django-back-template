# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog


class Permission(BaseModel):

    description        = models.CharField(max_length=255, blank=True, null=True)
        
    class Meta:
        db_table            = 'permissions'
        verbose_name        = 'permission'
        verbose_name_plural = 'permissions'


class PermissionLog(BaseLog):
    permission = models.ForeignKey('authentication.Permission', on_delete=models.CASCADE, related_name='permission_log_permission')
        
    class Meta:
        db_table            = 'permissions_logs'
        verbose_name        = 'permission_log'
        verbose_name_plural = 'permissions_logs'