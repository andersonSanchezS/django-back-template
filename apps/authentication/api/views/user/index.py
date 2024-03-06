# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.authentication.models import Users
# Serializers
from apps.authentication.api.serializers.user.index import UserSerializer
# Filters
from apps.authentication.api.filters.user.index import UserFilter
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin
from apps.base.decorators.checkPermissions import checkPermissions

class UserAV(FilterAndPaginationMixin,GenericAPIView):

    model            = Users
    serializer_class = UserSerializer
    filterset_class  = UserFilter
    
    @checkPermissions(['ADMINISTRADOR'],['VER USUARIO'])
    def get(self, request, pk=None):
        try:
            if pk:
                typeDocument = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(typeDocument)
                return response.success('Usuario obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Usuarios obtenidos correctamente', serializer.data)
        except Users.DoesNotExist:
            return response.failed('Usuario no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)

    @checkPermissions(['ADMINISTRADOR'],['CREAR USUARIO'])
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Usuario creado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
        
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR USUARIO'])
    def patch(self, request, pk=None):
        try:
            user = self.model.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Usuario actualizado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Users.DoesNotExist:
            return response.failed('Usuario no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
        
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR USUARIO'])
    def delete(self, request, pk=None):
        try:
            user = self.model.objects.get(pk=pk)
            user.state = False
            user.save()
            return response.success('Usuario eliminado exitosamente')
        except Users.DoesNotExist:
            return response.failed('Usuario no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
