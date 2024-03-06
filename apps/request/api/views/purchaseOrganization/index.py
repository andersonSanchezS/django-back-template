# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.request.models import PurchaseOrganization
# Serializers
from apps.request.api.serializers.purchaseOrganization.index import PurchaseOrganizationSerializer
# Filters
from apps.request.api.filters.purchaseOrganization.index import PurchaseOrganizationFilter
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin
from apps.base.decorators.checkPermissions import checkPermissions

class PurchaseOrganizationAV(FilterAndPaginationMixin, GenericAPIView):
    
    model            = PurchaseOrganization
    serializer_class = PurchaseOrganizationSerializer
    filterset_class  = PurchaseOrganizationFilter

    @checkPermissions(['ADMINISTRADOR'],['VER ORGANIZACION DE COMPRA'])
    def get(self, request, pk=None):
        try:
            if pk:
                data = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(data)
                return response.success('Organizacion de compra obtenida correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Organizaciones de compras obtenidas correctamente', serializer.data)
        except self.model.DoesNotExist:
            return response.failed('Organizacion de compra no encontrada', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
    
    @checkPermissions(['ADMINISTRADOR'],['CREAR ORGANIZACION DE COMPRA'])
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Organizacion de compra creada exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
        
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR ORGANIZACION DE COMPRA'])
    def patch(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            serializer = self.get_serializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Organizacion de compra actualizada exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except self.model.DoesNotExist:
            return response.failed('Organizacion de compra no encontrada', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR ORGANIZACION DE COMPRA'])
    def delete(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            data.state = 0
            data.save()
            return response.success('Organizacion de compra eliminada exitosamente')
        except self.model.DoesNotExist:
            return response.failed('Organizacion de compra no encontrada', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)