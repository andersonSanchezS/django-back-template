from django.http import JsonResponse
import logging
import ast 

# Configurar el logger para este middleware
logger = logging.getLogger(__name__)

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.handle_exception(request, e)

    def handle_exception(self, request, exception):
        logger.exception(f"Excepción no manejada capturada por CustomExceptionMiddleware: {exception}")
        return JsonResponse({'error': 'Se ha producido un error interno del servidor'}, status=500)
