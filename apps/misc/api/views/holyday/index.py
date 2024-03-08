# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.misc.models import Holyday
# Filters
from apps.misc.api.filters.holyday.index import HolydayFilter
# Serializers
from apps.misc.api.serializer.holyday.index import HolydaySerializer
# Utils
from apps.base.utils.index import response
from apps.base.decorators.checkPermissions import checkPermissions
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin


class HolydayAV(FilterAndPaginationMixin,GenericAPIView):

    model            = Holyday
    serializer_class = HolydaySerializer
    filterset_class  = HolydayFilter

    @checkPermissions(['ADMINISTRADOR'],['VER FESTIVO'])
    def get(self, request, pk=None):
        try:
            if pk:
                typeDocument = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(typeDocument)
                return response.success('Festivo obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Festivos obtenidos correctamente', serializer.data)
        except self.model.DoesNotExist:
            return response.failed('Festivo no encontrado', 404)
        except Exception as e:
            return response.failed(str(e), 500)

    @checkPermissions(['ADMINISTRADOR'],['CREAR FESTIVO'])
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Festivo creado correctamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0],400)
        except Exception as e:
            return response.failed(str(e), 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR FESTIVO'])
    def patch(self, request, pk=None):
        try:
            holyday = self.model.objects.get(pk=pk)
            serializer = self.get_serializer(holyday, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Festivo actualizado correctamente', serializer.data)
            else:
                return response.failed(serializer.errors)
        except self.model.DoesNotExist:
            return response.failed('Festivo no encontrado', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR FESTIVO'])
    def delete(self, request, pk=None):
        try:
            holyday       = self.model.objects.get(pk=pk)
            holyday.state = 0
            holyday.save()
            return response.success('Festivo eliminado correctamente', None)
        except self.model.DoesNotExist:
            return response.failed('Festivo no encontrado', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    