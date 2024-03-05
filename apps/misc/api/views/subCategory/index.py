# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.misc.models import SubCategory
# Filters
from apps.misc.api.filters.subCategory.index import SubCategoryFilter
# Serializers
from apps.misc.api.serializer.subCategory.index import SubCategorySerializer
# Utils
from apps.base.utils.index import response
from apps.base.decorators.checkPermissions import checkPermissions
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin


class SubCategoryAV(FilterAndPaginationMixin,GenericAPIView):

    model            = SubCategory
    serializer_class = SubCategorySerializer
    filterset_class  = SubCategoryFilter

    @checkPermissions(['ADMINISTRADOR'],['VER SUB CATEGORÍA'])
    def get(self, request, pk=None):
        try:
            if pk:
                subCategory = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(subCategory)
                return response.success('Sub categoría obtenida correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Sub categorías obtenidas correctamente', serializer.data)
        except self.model.DoesNotExist:
            return response.failed('Sub categoría no encontrada', 404)
        except Exception as e:
            return response.failed(str(e), 500)

    @checkPermissions(['ADMINISTRADOR'],['CREAR SUB CATEGORÍA'])
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Sub categoría creada correctamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0],400)
        except Exception as e:
            return response.failed(str(e), 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR SUB CATEGORÍA'])
    def patch(self, request, pk=None):
        try:
            subCategory = self.model.objects.get(pk=pk)
            serializer  = self.get_serializer(subCategory, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Sub categoría actualizada correctamente', serializer.data)
            else:
                return response.failed(serializer.errors)
        except self.model.DoesNotExist:
            return response.failed('Sub categoría no encontrada', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR SUB CATEGORÍA'])
    def delete(self, request, pk=None):
        try:
            subCategory       = self.model.objects.get(pk=pk)
            subCategory.state = 0
            subCategory.save()
            return response.success('Sub categoría eliminada correctamente', None)
        except self.model.DoesNotExist:
            return response.failed('Sub categoría no encontrada', 404)
        except Exception as e:
            return response.failed(str(e), 500)
    