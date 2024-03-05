# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class SubCategory(BaseModel):

    code         = models.CharField(max_length=10, blank=False, null=False, unique=True)
    description  = models.CharField(max_length=255, blank=False, null=False, unique=True)
    category     = models.ForeignKey('misc.category', on_delete=models.CASCADE)

    class Meta:
        db_table            = 'sub_categories'
        verbose_name        = 'sub_category'
        verbose_name_plural = 'sub_categories'


class SubCategoryLog(BaseLog):
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'sub_categories_log'
        verbose_name        = 'sub_category_log'
        verbose_name_plural = 'sub_categories_log'

    1