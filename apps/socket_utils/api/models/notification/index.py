# Rest framework
from django.db import models
# Models
from apps.base.models import GenericModel
# Enums
from apps.socket_utils.enums import NotificationTypeEnum


class Notification(GenericModel):

    sender_user    = models.ForeignKey('authentication.users',related_name='notifications_sent',on_delete=models.CASCADE, help_text='Hace referencia a el usuario remitente',null=True)
    receiving_user = models.ForeignKey('authentication.users', related_name='notifications_received',on_delete=models.CASCADE,help_text='Hace referencia a el usuario receptor')
    type           = models.CharField(max_length=255, choices=NotificationTypeEnum.choices(), default=NotificationTypeEnum.NEW_SOLCOT.value,  help_text='Hace referencia al tipo de notificación')
    title          = models.CharField(max_length=255, help_text='Hace referencia al titulo de la notificación')
    message        = models.TextField(help_text='Hace referencia al mensaje de la notificación')
    button_text    = models.CharField(max_length=255, help_text='Hace referencia al texto del botón de la notificación')
    button_link    = models.CharField(max_length=255, help_text='Hace referencia al link del botón de la notificación')
    icon           = models.CharField(max_length=255, help_text='Hace referencia al icono de la notificación')
    viewed         = models.BooleanField(default=False, help_text='Hace referencia a si la notificación fue vista o no')
    
    class Meta:
        db_table            = 'notifications'
        verbose_name        = 'notification'
        verbose_name_plural = 'notifications'