import django_filters
from   apps.request.models import ShoppingGroup
from apps.base.filters import SubstringFilter

class ShoppingGroupFilter(django_filters.FilterSet):

    description = SubstringFilter()
    code        = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = ShoppingGroup
        fields = ['description', 'code', 'state']
