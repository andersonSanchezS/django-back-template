# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.misc.models import Category
# Filters
from apps.misc.api.filters.category.index import CategoryFilter
# Serializers
from apps.misc.api.serializer.category.index import CategorySerializer
# Utils
from apps.base.utils.index import response
from apps.base.decorators.checkPermissions import checkPermissions
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin


class CategoryAV(FilterAndPaginationMixin,GenericAPIView):

    model            = Category
    serializer_class = CategorySerializer
    filterset_class  = CategoryFilter

    @checkPermissions(['ADMINISTRADOR'],['VER CATEGORÍA'])
    def get(self, request, pk=None):
        try:
            if pk:
                category = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(category)
                return response.success('Categoría obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Categorías obtenidas correctamente', serializer.data)
        except self.model.DoesNotExist:
            return response.failed('Categoría no encontrada', 404)
        except Exception as e:
            return response.failed(str(e), 500)

    @checkPermissions(['ADMINISTRADOR'],['CREAR CATEGORÍA'])
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Categoría creada correctamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0],400)
        except Exception as e:
            return response.failed(str(e), 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR CATEGORÍA'])
    def patch(self, request, pk=None):
        try:
            category = self.model.objects.get(pk=pk)
            serializer = self.get_serializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Categoría actualizada correctamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0],400)
        except self.model.DoesNotExist:
            return response.failed('Categoría no encontrada', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR CATEGORÍA'])
    def delete(self, request, pk=None):
        try:
            category       = self.model.objects.get(pk=pk)
            category.state = 0
            category.save()
            return response.success('Categoría eliminada correctamente', None)
        except self.model.DoesNotExist:
            return response.failed('Categoría no encontrada', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    