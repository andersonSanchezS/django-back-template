# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.authentication.models import Menu
# Serializers
from apps.authentication.api.serializers.menu.index import MenuSerializer
# Filters
from apps.authentication.api.filters.menu.index import MenuFilter
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin
from apps.base.decorators.checkPermissions import checkPermissions

class MenuAV(FilterAndPaginationMixin, GenericAPIView):
    
    model            = Menu
    serializer_class = MenuSerializer
    filterset_class  = MenuFilter

    @checkPermissions(['ADMINISTRADOR'],['VER MENU'])
    def get(self, request, pk=None):
        try:
            if pk:
                data = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(data)
                return response.success('Menu obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Menus obtenidos correctamente', serializer.data)
        except self.model.DoesNotExist:
            return response.failed('Menu no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
    
    @checkPermissions(['ADMINISTRADOR'],['CREAR MENU'])
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Menu creado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
        
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR MENU'])
    def patch(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            serializer = self.get_serializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Menu actualizado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except self.model.DoesNotExist:
            return response.failed('Menu no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR MENU'])
    def delete(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            data.state = 0
            data.save()
            return response.success('Menu eliminado exitosamente')
        except self.model.DoesNotExist:
            return response.failed('Menu no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)