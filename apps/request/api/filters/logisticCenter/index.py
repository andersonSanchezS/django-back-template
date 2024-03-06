import django_filters
from   apps.request.models import LogisticCenter
from apps.base.filters     import SubstringFilter

class LogisticCenterFilter(django_filters.FilterSet):

    description = SubstringFilter()
    code        = SubstringFilter()
    
    class Meta:
        model  = LogisticCenter
        fields = ['description', 'code']
