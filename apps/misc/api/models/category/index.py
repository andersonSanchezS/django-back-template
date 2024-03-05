# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class Category(BaseModel):
    code         = models.CharField(max_length=10, blank=False, null=False, unique=True,  error_messages={'unique': 'Ya existe una categoría con este código'})
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe una categoría con este nombre'})

    class Meta:
        db_table            = 'categories'
        verbose_name        = 'category'
        verbose_name_plural = 'categories'


class CategoryLog(BaseLog):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'categories_log'
        verbose_name        = 'category_log'
        verbose_name_plural = 'categories_log'

    