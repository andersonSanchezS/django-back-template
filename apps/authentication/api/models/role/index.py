# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog


class Role(BaseModel):
    description    = models.CharField(max_length=255)
    permissions    = models.ManyToManyField('authentication.permission', related_name='roles_clearpermission', blank=True)
    menus          = models.ManyToManyField('authentication.menu', related_name='roles_menu', blank=True)

    class Meta:
        db_table            = 'roles'
        verbose_name        = 'role'
        verbose_name_plural = 'roles'


class RoleLog(BaseLog):
    role = models.ForeignKey('authentication.Role', on_delete=models.CASCADE, related_name='role_log_role')        
    class Meta:
        db_table            = 'roles_logs'
        verbose_name        = 'role_log'
        verbose_name_plural = 'roles_logs'