import django_filters
from   apps.misc.models import TypeDocument
from apps.base.filters import SubstringFilter

class TypeDocumentFilter(django_filters.FilterSet):
    description = SubstringFilter()
    state       = django_filters.BooleanFilter()
    class Meta:
        model  = TypeDocument
        fields = ['description', 'state']
