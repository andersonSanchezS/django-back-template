import django_filters
from   apps.authentication.models import Menu
from apps.base.filters import SubstringFilter

class MenuFilter(django_filters.FilterSet):

    description = SubstringFilter()
    
    class Meta:
        model  = Menu
        fields = ['description']