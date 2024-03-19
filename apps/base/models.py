from   django.db       import models
from   datetime        import datetime as dt
from   django.apps     import apps
from   apps.base.enums import LogActionsEnum
from   django.core     import serializers
import ulid
import time
import json
from django.core.cache import cache
# Exceptions
from apps.base.exceptions import HTTPException

# 
# BASE MODEL FOR ALL LOGS
class BaseLog(models.Model):
    action_time    = models.DateTimeField(auto_now=True)
    user           = models.ForeignKey('authentication.Users', on_delete=models.CASCADE)
    action         = models.CharField(max_length=255)
    previousValues = models.JSONField(null=True, blank=True)
    newValues      = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True

# BASE MODEL FOR ALL ENTITIES 
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
        try:

            if not self.id:
                self.id = ulid.new().str

            if not self.created_at_unix:
                self.created_at = dt.now()
                self.created_at_unix = int(time.time())

            self.updated_at_unix = int(time.time())
            self.updated_at = dt.now()

            app        = self._meta.app_label
            className  = self.__class__.__name__+'Log'
            # get the model instance from the app
            model      = apps.get_model(app, className)
            # parse to camel case
            logRelation = {
                self.__class__.__name__[0].lower() + self.__class__.__name__[1:] : self
            }
            if self._state.adding:
                # get the data of the fields except _state
                fields = serializers.serialize('json', [self,])
                action = LogActionsEnum.CREATE.value
                user   = self.user_created_at
                super(BaseModel, self).save(*args, **kwargs)
                model.objects.create( action_time=dt.now(), user=user, action=action, newValues=json.loads(fields), previousValues=None, **logRelation)
            else:
                baseFields = ['id', 'created_at', 'updated_at', 'created_at_unix', 'updated_at_unix', 'user_updated_at_id', 'user_created_at_id','_state']
                # filter the fields and remove the fields who are in the baseFields list
                fields     = {k:v for k,v in self.__dict__.items() if k not in baseFields}
                action = LogActionsEnum.UPDATE.value
                user   = self.user_updated_at
                previousData = self.__class__.objects.get(id=self.id)
                # compare the new data with the previous data and get the fields that have changed
                newFields = {k:v for k,v in fields.items() if getattr(previousData, k) != v}
                # based on the new data get the fields that have changed and get the previous value
                previousFields = {k:getattr(previousData, k) for k,v in newFields.items()}                
                # compare the state of the previous data with the new data
                if 'state' in previousFields and 'state' in newFields:
                    if previousFields['state'] == 1 and newFields['state'] == 0:
                        action = LogActionsEnum.DELETE.value
                    elif previousFields['state'] == 0 and newFields['state'] == 1:
                        action = LogActionsEnum.RESTORE.value
                model.objects.create( action_time=dt.now(), user=user, action=action, newValues=newFields, previousValues=previousFields, **logRelation)
                super(BaseModel, self).save(*args, **kwargs)
        except Exception as e:
            raise HTTPException(str(e), 500)
        
# BASE MODEL FOR ALL REQUEST LOGS
class RequestLog(models.Model):
    ip           = models.CharField(max_length=255)
    method       = models.CharField(max_length=255)
    path         = models.CharField(max_length=255)
    body         = models.TextField(null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    client       = models.CharField(max_length=255, null=True, blank=True)
    user         = models.ForeignKey('authentication.Users', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table            = 'request_logs'
        verbose_name        = 'request_log'
        verbose_name_plural = 'request_logs'

# GENERIC FUNCTION TO TRACK THE CHANGES OF MANY TO MANY FIELDS
def track_m2m_field_changes(sender, instance, action, reverse, model, pk_set, logModel, **kwargs):
    cache_key = f"m2m_{instance.pk}_{ulid.new().str}"
    
    if action == "pre_add":
        existing_pks = set(instance.sub_categories.values_list('pk', flat=True))
        cache.set(cache_key, list(existing_pks), 300)

    elif action == "post_add":
            
        previous_pks = cache.get(cache_key, [])
        new_pks = set(pk_set) - set(previous_pks)
        cache.delete(cache_key)

        for field in instance._meta.get_fields():
            if field.many_to_many and field.remote_field.through == sender:
                field_name = field.name
                break

        newValues = {f'{field_name}': list(new_pks)}
        previousValues = {f'{field_name}': list(previous_pks)}


        logModel.objects.create(
            user=instance.user_updated_at if previous_pks else instance.user_created_at,
            action=LogActionsEnum.UPDATE.value if previous_pks else LogActionsEnum.CREATE.value,
            newValues=json.dumps(newValues),
            previousValues=json.dumps(previousValues),
            solcot=instance
        )   