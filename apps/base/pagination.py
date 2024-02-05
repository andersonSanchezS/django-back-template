from rest_framework.pagination import LimitOffsetPagination

class CustomPagination(LimitOffsetPagination):
    default_limit = 10  
    max_limit     = 100

    def get_limit(self, request):
        limit = request.query_params.get('limit', self.default_limit)
        try:
            return min(int(limit), self.max_limit)
        except ValueError:
            return self.default_limit