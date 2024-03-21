# Utils
from channels.db import database_sync_to_async
from django.utils import timezone

@database_sync_to_async
def get_token(self, model,tokenString):
    token = model.objects.filter(token=tokenString, is_valid=1).first()
    if not token:
        return None
    
    return {
        'expiration': token.expiration,
        'user': token.user.id   
    }


def invalidate_token(self, token):
    token.is_valid = 0
    token.save()
    return None


@database_sync_to_async
def make_aware_async(naive_datetime):
    return timezone.make_aware(naive_datetime, timezone.get_default_timezone())