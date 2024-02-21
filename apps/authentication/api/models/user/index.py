# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog


class Users(BaseModel):

    first_name         = models.CharField(max_length=255, verbose_name='first name', blank=False, null=False)
    last_name          = models.CharField(max_length=255, verbose_name='last name', blank=False, null=False)
    type_document      = models.ForeignKey('misc.TypeDocument', on_delete=models.CASCADE, related_name='users_type_document', blank=False, null=False)
    document_number    = models.CharField(max_length=255, verbose_name='document_number', blank=False, null=False)
    email              = models.EmailField(max_length=255, verbose_name='Email', unique=True)
    username           = models.CharField(max_length=255, verbose_name='username', unique=True, null=True, blank=True)
    password           = models.CharField(max_length=255, verbose_name='password', null=True, blank=True)
    phone_number       = models.CharField(max_length=255, verbose_name='phone_number', blank=True, null=True)
    is_ldap_user       = models.BooleanField(default=False)
    is_superuser       = models.BooleanField(default=False)
    roles              = models.ManyToManyField('authentication.role', related_name='users_role', blank=True)
    categories         = models.ManyToManyField('misc.category', related_name='users_category', blank=True)
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