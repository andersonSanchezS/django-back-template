from django.db import models
import ulid
import time
from datetime import datetime as dt
from django.core import serializers

class ActivityLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    model      = models.CharField(max_length=255)
    action     = models.CharField(max_length=255)
    user       = models.ForeignKey('authentication.Users', on_delete=models.CASCADE, related_name='%(class)s_created_at', null=True, default=None)
    data       = models.JSONField(null=True, blank=True)

    class Meta:
        db_table            = 'activity_logs'
        verbose_name        = 'activity_log'
        verbose_name_plural = 'activity_log'


class BaseModel(models.Model):
    id              = models.CharField(max_length=255, unique=True, primary_key=True, editable=False)
    state           = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    created_at_unix = models.BigIntegerField(editable=False)
    updated_at_unix = models.BigIntegerField(null=True, editable=False)
    user_created_at = models.ForeignKey('authentication.Users', on_delete=models.CASCADE, related_name='%(class)s_created_at', null=True, default=None)
    user_updated_at = models.ForeignKey('authentication.Users', on_delete=models.CASCADE, related_name='%(class)s_updated_at', null=True, default=None)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ulid.new().str

        if not self.created_at_unix:
            self.created_at = dt.now()
            self.created_at_unix = int(time.time())

        self.updated_at_unix = int(time.time())
        self.updated_at = dt.now()

        super(BaseModel, self).save(*args, **kwargs)

        # Crear registro en el log
        try:
            # Parse the data into a json
            jsonData = serializers.serialize('json', [self, ])
            ActivityLog.objects.create(
                model=self.__class__.__name__,
                action='CREATE',
                user=self.user_created_at,
                data=jsonData
            )
        except Exception as e:
            print(e)


    def update(self, *args, **kwargs):
        # Actualizar siempre updated_at_unix
        self.updated_at_unix = int(time.time())

        super(BaseModel, self).update(*args, **kwargs)
