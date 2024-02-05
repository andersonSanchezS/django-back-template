from django_filters import CharFilter
from django.db.models import Q


class SubstringFilter(CharFilter):
    def filter(self, qs, value):
        if value not in (None, ''):
            qs = qs.filter(Q(description__iregex=r"" + value))
        return qs