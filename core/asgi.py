import os

from django.core.asgi import get_asgi_application


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth    import AuthMiddlewareStack
import core.routing
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})
