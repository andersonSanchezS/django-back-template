import django_filters
from   apps.authentication.models import Users, Role
from   apps.misc.models import Category
from   apps.base.filters import SubstringFilter

class UserFilter(django_filters.FilterSet):
    first_name  = SubstringFilter()
    last_name   = SubstringFilter()
    email       = SubstringFilter()
    role        = django_filters.ModelMultipleChoiceFilter(queryset=Role.objects.all(), field_name='roles', conjoined=True)
    category    = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), field_name='categories', conjoined=True)
    state       = django_filters.BooleanFilter()
    class Meta:
        model  = Users
        fields = ['first_name' ,'last_name' ,'email', 'role', 'state']
