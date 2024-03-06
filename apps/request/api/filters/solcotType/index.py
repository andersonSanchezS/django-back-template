import django_filters
from   apps.request.models import SolcotType
from apps.base.filters import SubstringFilter

class SolcotTypeFilter(django_filters.FilterSet):

    description = SubstringFilter()
    days        = django_filters.NumberFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = SolcotType
        fields = ['description', 'days', 'state']
