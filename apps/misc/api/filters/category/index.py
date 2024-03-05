import django_filters
from   apps.misc.models import Category
from apps.base.filters import SubstringFilter

class CategoryFilter(django_filters.FilterSet):
    description = SubstringFilter()
    code        = SubstringFilter()

    class Meta:
        model  = Category
        fields = ['description', 'code']
