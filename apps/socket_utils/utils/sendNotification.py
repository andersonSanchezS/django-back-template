from apps.socket_utils.models import Notification
# Socket
from asgiref.sync    import async_to_sync
from channels.layers import get_channel_layer

def sendNotification(sender_user, receiving_user, type, title, message, button_text, button_link, icon):
    # Create notification
    notification = Notification.objects.create(
        sender_user=sender_user,
        receiving_user=receiving_user,
        type=type,
        title=title,
        message=message,
        button_text=button_text,
        button_link=button_link,
        icon=icon
    )

    # Send notification to user
    channelLayer    = get_channel_layer()
    receivingUserId = receiving_user.id
    roomName        = f'notification_{receivingUserId}'
    async_to_sync(channelLayer.group_send)(
        roomName,
        {
            'type': 'notification_message',
            'message': {
                'type': notification.type,
                'title': notification.title,
                'message': notification.message,
                'button_text': notification.button_text,
                'button_link': notification.button_link,
                'icon': notification.icon,
            }
        }
    )
