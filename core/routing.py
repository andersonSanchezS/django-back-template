from django.urls import re_path
from .websocket.notificationConsumer import NotificationConsumer
import django



websocket_urlpatterns = [
    re_path(r'ws/notifications', NotificationConsumer.as_asgi()),
]
