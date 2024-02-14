# Rest framework
from django.db import models


class Token(models.Model):
    id           = models.CharField(max_length=255, primary_key=True)
    token        = models.TextField()
    user         = models.ForeignKey('authentication.users', on_delete=models.CASCADE, related_name='token_user_auth')
    is_valid     = models.BooleanField(default=True)
    expiration   = models.DateTimeField()
    created_at   = models.DateTimeField(auto_now_add=True)    
        
    class Meta:
        db_table            = 'tokens'
        verbose_name        = 'token'
        verbose_name_plural = 'tokens'
