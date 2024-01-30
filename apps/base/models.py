from django.db import models
import ulid
import time

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

        # Asignar timestamp Unix a created_at_unix si es una nueva instancia
        if not self.created_at_unix:
            self.created_at_unix = int(time.time())

        # Actualizar siempre updated_at_unix
        self.updated_at_unix = int(time.time())

        super(BaseModel, self).save(*args, **kwargs)

        # crear un registro en tabla de auditoria

    def update(self, *args, **kwargs):
        # Actualizar siempre updated_at_unix
        self.updated_at_unix = int(time.time())

        super(BaseModel, self).update(*args, **kwargs)