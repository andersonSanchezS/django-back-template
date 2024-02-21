# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog



class TypeDocument(BaseModel):

    description  = models.CharField(max_length=255, blank=False, null=False, unique=True)
    abbreviation = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        db_table            = 'type_documents'
        verbose_name        = 'type_document'
        verbose_name_plural = 'type_documents'


class TypeDocumentLog(BaseLog):
    typeDocument = models.ForeignKey(TypeDocument, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'type_documents_log'
        verbose_name        = 'type_document_log'
        verbose_name_plural = 'type_documents_log'

    