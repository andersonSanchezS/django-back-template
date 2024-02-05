from django_filters.rest_framework import DjangoFilterBackend
from apps.base.pagination import CustomPagination

class FilterAndPaginationMixin:
    filter_backends  = [DjangoFilterBackend]
    filterset_class  = None
    pagination_class = CustomPagination
    paginator        = None


    def paginate_queryset(self, queryset):

        if self.pagination_class is None:
            return None
        self.paginator = self.pagination_class()
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert hasattr(self, 'paginator')
        return self.paginator.get_paginated_response(data)


    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if hasattr(self, 'queryset'):
            queryset = self.queryset
            if hasattr(queryset, 'all'):
                queryset = queryset.all()
        elif hasattr(self, 'model'):
            queryset = self.model.objects.all()
        else:
            raise NotImplementedError("Debes definir 'queryset' o 'model' en tu vista.")
        
        return self.filter_queryset(queryset)