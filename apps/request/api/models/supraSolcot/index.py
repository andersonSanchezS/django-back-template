# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog
# Enums
from apps.request.enums import ProcessStateEnum



class SupraSolcot(BaseModel):
    solcot_type           = models.ForeignKey('request.solcotType', on_delete=models.CASCADE)
    client_email          = models.EmailField(max_length=255, blank=False, null=False)
    viewed_by_buyer       = models.BooleanField(default=False)
    accepted_at           = models.DateTimeField(blank=True, null=True)
    finished_at           = models.DateTimeField(blank=True, null=True)
    process_state         = models.CharField(max_length=255, choices=ProcessStateEnum.choices(), default=ProcessStateEnum.PENDING.value)
    logistic_center       = models.ForeignKey('request.logisticCenter', on_delete=models.CASCADE)
    shopping_group        = models.ForeignKey('request.shoppingGroup', on_delete=models.CASCADE)
    purchase_organization = models.ForeignKey('request.purchaseOrganization', on_delete=models.CASCADE)
    category              = models.ForeignKey('misc.category', on_delete=models.CASCADE)
    client                = models.ForeignKey('authentication.users', on_delete=models.CASCADE, related_name='supra_solcot_client')


    class Meta:
        db_table            = 'supra_solcot'
        verbose_name        = 'supra_solcot'
        verbose_name_plural = 'supra_solcot'


class SupraSolcotLog(BaseLog):
    supraSolcot = models.ForeignKey(SupraSolcot, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'supra_solcot_log'
        verbose_name        = 'supra_solcot_log'
        verbose_name_plural = 'supra_solcot_log'

    