import django_filters
from   apps.misc.models import Holyday
from apps.base.filters import SubstringFilter

class HolydayFilter(django_filters.FilterSet):
    description = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = Holyday
        fields = ['description', 'state']
