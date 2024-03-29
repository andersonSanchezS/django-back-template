import django_filters
from   apps.authentication.models import Users
from apps.base.filters import SubstringFilter

class UserFilter(django_filters.FilterSet):
    first_name  = SubstringFilter()
    last_name   = SubstringFilter()
    email       = SubstringFilter()
    class Meta:
        model  = Users
        fields = ['first_name' ,'last_name' ,'email']
