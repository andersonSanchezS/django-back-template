import django_filters
from   apps.authentication.models import Permission
from apps.base.filters import SubstringFilter

class PermissionFilter(django_filters.FilterSet):

    description = SubstringFilter()
    
    class Meta:
        model  = Permission
        fields = ['description']
