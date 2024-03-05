# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.authentication.models import Permission
# Serializers
from apps.authentication.api.serializers.permission.index import PermissionSerializer
# Filters
from apps.authentication.api.filters.permission.index import PermissionFilter
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin
from apps.base.decorators.checkPermissions import checkPermissions

class PermissionAV(FilterAndPaginationMixin, GenericAPIView):
    
    model            = Permission
    serializer_class = PermissionSerializer
    filterset_class  = PermissionFilter

    @checkPermissions(['ADMINISTRADOR'],['VER PERMISO'])
    def get(self, request, pk=None):
        try:
            if pk:
                data = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(data)
                return response.success('Permiso obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Permisos obtenidos correctamente', serializer.data)
        except Permission.DoesNotExist:
            return response.failed('Permiso no encontrado', 404)
        except Exception as e:
            return response.failed(e.message,e.status_code)
    
    @checkPermissions(['ADMINISTRADOR'],['CREAR PERMISO'])
    def post(self, request):
        try:
            serializer = PermissionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Permiso creado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Exception as e:
            return response.failed(e.message,e.status_code)
        
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR PERMISO'])
    def patch(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            serializer = PermissionSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Permiso actualizado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Permission.DoesNotExist:
            return response.failed('Permiso no encontrado', 404)
        except Exception as e:
            return response.failed(e.message,e.status_code)
    
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR PERMISO'])
    def delete(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            data.state = 0
            data.save()
            return response.success('Permiso eliminado exitosamente')
        except Permission.DoesNotExist:
            return response.failed('Permiso no encontrado', 404)
        except Exception as e:
            return response.failed(e.message,e.status_code)