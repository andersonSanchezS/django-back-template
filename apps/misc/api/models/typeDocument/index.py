# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel
# Validators
from django.core.validators import BaseValidator



class TypeDocument(BaseModel):

    description = models.CharField(max_length=255, blank=False, null=False, unique=True)
    class Meta:
        db_table            = 'type_documents'
        verbose_name        = 'type_document'
        verbose_name_plural = 'type_documents'