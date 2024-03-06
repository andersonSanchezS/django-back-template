import django_filters
from   apps.misc.models import SubCategory, Category
from apps.base.filters import SubstringFilter

class SubCategoryFilter(django_filters.FilterSet):
    
    description = SubstringFilter()
    code        = SubstringFilter()
    category    = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), field_name='category')
    state       = django_filters.BooleanFilter()

    class Meta:
        model  = SubCategory
        fields = ['description', 'code', 'category', 'state']
