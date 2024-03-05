# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.authentication.models import Role
# Serializers
from apps.authentication.api.serializers.role.index import RoleSerializer
# Filters
from apps.authentication.api.filters.role.index import RoleFilter
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin
from apps.base.decorators.checkPermissions import checkPermissions

class RoleAV(FilterAndPaginationMixin, GenericAPIView):

    model            = Role
    serializer_class = RoleSerializer
    filterset_class  = RoleFilter

    @checkPermissions(['ADMINISTRADOR'],['VER ROL'])
    def get(self, request, pk=None):
        try:
            if pk:
                data = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(data)
                return response.success('Rol obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Roles obtenidos correctamente', serializer.data)
        except Role.DoesNotExist:
            return response.failed('Rol no encontrado', 404)
        except Exception as e:
            return response.failed(e.message,e.status_code)
        
    @checkPermissions(['ADMINISTRADOR'],['CREAR ROL'])
    def post(self, request):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Rol creado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Exception as e:
            return response.failed(e.message,e.status_code)
        
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR ROL'])
    def patch(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            serializer = RoleSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Rol actualizado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Role.DoesNotExist:
            return response.failed('Rol no encontrado', 404)
        except Exception as e:
            return response.failed(e.message,e.status_code)
        
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR ROL'])
    def delete(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            data.state = 0
            data.save()
            return response.success('Rol eliminado exitosamente', None)
        except Role.DoesNotExist:
            return response.failed('Rol no encontrado', 404)
        except Exception as e:
            return response.failed(e.message,e.status_code)