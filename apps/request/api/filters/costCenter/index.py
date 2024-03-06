import django_filters
from   apps.request.models import CostCenter
from apps.base.filters     import SubstringFilter

class CostCenterFilter(django_filters.FilterSet):

    description = SubstringFilter()
    code        = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = CostCenter
        fields = ['description', 'code', 'state']
