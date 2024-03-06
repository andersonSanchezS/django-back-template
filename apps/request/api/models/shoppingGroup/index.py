# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class ShoppingGroup(BaseModel):
    code         = models.CharField(max_length=10, blank=True, null=True, unique=True,  error_messages={'unique': 'Ya existe una grupo de compra con este código'})
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe una grupo de compra con este nombre'})

    class Meta:
        db_table            = 'shopping_groups'
        verbose_name        = 'shopping_group'
        verbose_name_plural = 'shopping_groups'


class ShoppingGroupLog(BaseLog):
    shoppingGroup = models.ForeignKey(ShoppingGroup, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'shopping_groups_log'
        verbose_name        = 'shopping_group_log'
        verbose_name_plural = 'shopping_groups_log'

    