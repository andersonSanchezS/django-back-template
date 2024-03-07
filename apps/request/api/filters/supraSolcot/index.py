import django_filters
from   apps.request.models import SupraSolcot
from apps.base.filters import SubstringFilter
from apps.request.models import SolcotType, LogisticCenter, ShoppingGroup, PurchaseOrganization
from apps.misc.models import Category

class SupraSolcotFilter(django_filters.FilterSet):

    client_email          = SubstringFilter()
    accepted_at           = django_filters.DateFromToRangeFilter(field_name='accepted_at')
    finished_at           = django_filters.DateFromToRangeFilter(field_name='finished_at')
    solcot_type           = django_filters.ModelChoiceFilter(queryset=SolcotType.objects.all(), field_name='solcot_type__id')
    logistic_center       = django_filters.ModelChoiceFilter(queryset=LogisticCenter.objects.all(), field_name='logistic_center__id')
    shopping_group        = django_filters.ModelChoiceFilter(queryset=ShoppingGroup.objects.all(), field_name='shopping_group__id')
    purchase_organization = django_filters.ModelChoiceFilter(queryset=PurchaseOrganization.objects.all(), field_name='purchase_organization__id')
    category              = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), field_name='category__id')
    
    class Meta:
        model  = SupraSolcot
        fields = ['client_email', 'accepted_at', 'finished_at', 'solcot_type',
                  'logistic_center', 'shopping_group', 'purchase_organization',
                  'category']
