# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog


class Menu(BaseModel):

    description = models.CharField(max_length=255)
    icon        = models.CharField(max_length=255)
    url         = models.CharField(max_length=255)
        
    class Meta:
        db_table            = 'menus'
        verbose_name        = 'menu'
        verbose_name_plural = 'menus'


class MenuLog(BaseLog):
    menu = models.ForeignKey('authentication.menu', on_delete=models.CASCADE, related_name='menu_log_menu')
        
    class Meta:
        db_table            = 'menus_logs'
        verbose_name        = 'menu_log'
        verbose_name_plural = 'menus_logs'