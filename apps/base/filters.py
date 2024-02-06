from django_filters import CharFilter
from django.db.models import Q


class SubstringFilter(CharFilter):
    def filter(self, qs, value):
        if value not in (None, ''):
            qs = qs.filter(Q(**{f"{self.field_name}__iregex": r"" + value}))
        return qs