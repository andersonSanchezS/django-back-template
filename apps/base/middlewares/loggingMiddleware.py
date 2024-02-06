from datetime import datetime as dt
from apps.base.models import RequestLog

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Intenta obtener la dirección IP real del cliente desde `X-Forwarded-For` primero
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # obtiene el método de la solicitud
        method = request.method
        # obtiene la ruta de la solicitud
        path = request.path
        # obtiene el cuerpo de la solicitud
        body = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            body = request.body.decode('utf-8')
        # obtener la hora actual
        now = dt.now()

        # crea un registro de solicitud
        RequestLog.objects.create(
            ip=ip,
            method=method,
            path=path,
            body=body,
            request_date=now,
            user=request._user
        )

        response = self.get_response(request)
        return response