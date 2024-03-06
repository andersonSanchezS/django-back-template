import django_filters
from   apps.request.models import PurchaseOrganization
from apps.base.filters import SubstringFilter

class PurchaseOrganizationFilter(django_filters.FilterSet):

    description = SubstringFilter()
    code        = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = PurchaseOrganization
        fields = ['description', 'code', 'state']
