import django_filters
from apps.socket_utils.models import Notification
from apps.base.filters        import SubstringFilter

class NotificationFilter(django_filters.FilterSet):

    description = SubstringFilter()
    code        = SubstringFilter()
    state       = django_filters.BooleanFilter()
    
    class Meta:
        model  = Notification
        fields = ['description', 'code', 'state']
