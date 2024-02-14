# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog


class Users(BaseModel):

    first_name         = models.CharField(max_length=255, verbose_name='first name', blank=True, null=True)
    last_name          = models.CharField(max_length=255, verbose_name='last name', blank=True, null=True)
    description        = models.CharField(max_length=255, blank=True, null=True)
    email              = models.EmailField(max_length=255, verbose_name='Email', unique=True)
    username           = models.CharField(max_length=255, verbose_name='username', unique=True, null=True, blank=True)
    password           = models.CharField(max_length=255, verbose_name='password', null=True, blank=True)
    is_superuser       = models.BooleanField(default=False)
    roles              = models.ManyToManyField('authentication.role', related_name='users_role', blank=True)
    custom_permissions = models.ManyToManyField('authentication.permission', related_name='users_custom_permission', blank=True)
    
    class Meta:
        db_table            = 'users'
        verbose_name        = 'user'
        verbose_name_plural = 'users'


class UsersLog(BaseLog):

    users = models.ForeignKey('authentication.Users', on_delete=models.CASCADE, related_name='users_log_user')
    
    class Meta:
        db_table            = 'users_logs'
        verbose_name        = 'user_log'
        verbose_name_plural = 'users_logs'