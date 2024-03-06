import django_filters
from   apps.authentication.models import Role
from apps.base.filters import SubstringFilter

class RoleFilter(django_filters.FilterSet):

    description = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = Role
        fields = ['description', 'state']
