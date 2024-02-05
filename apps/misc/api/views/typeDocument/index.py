# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.misc.models import TypeDocument
# Serializers
from apps.misc.api.serializer.typeDocument.index import TypeDocumentSerializer
# Utils
from apps.base.utils.index import response


class TypeDocumentAV(GenericAPIView):

    def post(self, request):
        try:
            serializer = TypeDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Tipo de documento creado correctamente', serializer.data)
            else:
                return response.failed(serializer.errors)
        except Exception as e:
            return response.failed(e.message, e.status_code)
        
    def patch(self, request, pk=None):
        try:
            typeDocument = TypeDocument.objects.get(pk=pk)
            serializer = TypeDocumentSerializer(typeDocument, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Tipo de documento actualizado correctamente', serializer.data)
            else:
                return response.failed(serializer.errors)
        except Exception as e:
            return response.failed(e.message, e.status_code)
    