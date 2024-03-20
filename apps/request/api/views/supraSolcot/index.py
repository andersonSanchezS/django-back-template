# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.request.models import SupraSolcot, Solcot
# Serializers
from apps.request.api.serializers.supraSolcot.index import SupraSolcotSerializer
# Filters
from apps.request.api.filters.supraSolcot.index import SupraSolcotFilter
# Utils
from apps.base.utils.index import response
from apps.base.mixins.filterAndPaginationMixin import FilterAndPaginationMixin
from apps.base.decorators.checkPermissions import checkPermissions
from apps.request.enums import ProcessStateEnum

class SupraSolcotAV(FilterAndPaginationMixin, GenericAPIView):
    
    model            = SupraSolcot
    serializer_class = SupraSolcotSerializer
    filterset_class  = SupraSolcotFilter

    @checkPermissions(['ADMINISTRADOR'],['VER SUPRA SOLCOT'])
    def get(self, request, pk=None):
        try:
            if pk:
                data = self.model.objects.get(pk=pk)
                serializer   = self.get_serializer(data)
                return response.success('Supra solcot obtenido correctamente', serializer.data)
            else:
                queryset = self.get_queryset()
                if request.query_params.get('paginate') == 'true':
                    paginated_queryset = self.paginate_queryset(queryset)
                    serializer = self.get_serializer(paginated_queryset, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    serializer = self.get_serializer(queryset, many=True)
                    return response.success('Supra solcots obtenidos correctamente', serializer.data)
        except self.model.DoesNotExist:
            return response.failed('Supra solcot no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
    
    @checkPermissions(['ADMINISTRADOR'],['CREAR SUPRA SOLCOT'])
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.success('Supra solcot creado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
        
    @checkPermissions(['ADMINISTRADOR'],['ACTUALIZAR SUPRA SOLCOT'])
    def patch(self, request, pk=None):
        try:
            data = self.model.objects.get(pk=pk)
            serializer = self.get_serializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.success('Supra solcot actualizado exitosamente', serializer.data)
            else:
                return response.failed(serializer.errors[next(iter(serializer.errors))][0], 400)
        except self.model.DoesNotExist:
            return response.failed('Supra solcot no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)
    
            data.state = 0
    @checkPermissions(['ADMINISTRADOR'],['ELIMINAR SUPRA SOLCOT'])
    def delete(self, request, pk=None):
        try:
            # check the state of the supra solcot
            data = self.model.objects.get(pk=pk)
            if data.state == ProcessStateEnum.PENDING.value:
                return response.failed('No se puede eliminar un supra solcot que este en un estado diferente de pendiente', 400)
            data.state = 0
            data.user_updated_at = request._user
            data.save()
            # get the solcot and update the state
            solcots = Solcot.objects.filter(supra_solcot=data)
            for solcot in solcots:
                solcot.state = 0
                solcot.user_updated_at = request._user
                solcot.save()
            return response.success('Supra solcot eliminado exitosamente')
        except self.model.DoesNotExist:
            return response.failed('Supra solcot no encontrado', 404)
        except Exception as e:
            return response.failed(e.message if hasattr(e, 'message') else str(e), e.status_code if hasattr(e, 'status_code') else 500)