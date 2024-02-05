# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.misc.models import TypeDocument
# Filters
from apps.misc.api.filters.typeDocument.index import TypeDocumentFilter
# Serializers
from apps.misc.api.serializer.typeDocument.index import TypeDocumentSerializer
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin


class TypeDocumentAV(FilterAndPaginationMixin,GenericAPIView):

    model            = TypeDocument
    serializer_class = TypeDocumentSerializer
    filterset_class  = TypeDocumentFilter

    def get(self, request, pk=None):
        try:
            if pk:
                typeDocument = TypeDocument.objects.get(pk=pk)
                serializer   = TypeDocumentSerializer(typeDocument)
                return response.success('Tipo de documento obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Tipos de documento obtenidos correctamente', serializer.data)
        except TypeDocument.DoesNotExist:
            return response.failed('Tipo de documento no encontrado', 404)
        except Exception as e:
            return response.failed(str(e), 500)

    def post(self, request):
        try:
            serializer = TypeDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Tipo de documento creado correctamente', serializer.data)
            else:
                return response.failed(serializer.errors)
        except Exception as e:
            return response.failed(str(e), 500)
        
    def patch(self, request, pk=None):
        try:
            typeDocument = TypeDocument.objects.get(pk=pk)
            serializer = TypeDocumentSerializer(typeDocument, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Tipo de documento actualizado correctamente', serializer.data)
            else:
                return response.failed(serializer.errors)
        except TypeDocument.DoesNotExist:
            return response.failed('Tipo de documento no encontrado', 404)
        except Exception as e:
            return response.failed(str(e), 500)
        
    def delete(self, request, pk=None):
        try:
            typeDocument       = TypeDocument.objects.get(pk=pk)
            typeDocument.state = 0
            typeDocument.save()
            return response.success('Tipo de documento eliminado correctamente', None)
        except TypeDocument.DoesNotExist:
            return response.failed('Tipo de documento no encontrado', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    