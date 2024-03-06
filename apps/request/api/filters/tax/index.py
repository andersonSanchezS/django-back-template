import django_filters
from   apps.request.models import Tax
from apps.base.filters import SubstringFilter

class TaxFilter(django_filters.FilterSet):

    description = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = Tax
        fields = ['description', 'state']
