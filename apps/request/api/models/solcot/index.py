# Rest framework
from django.db import models
# Models
from apps.base.models import BaseModel, BaseLog
# Enums
from apps.request.enums import ProcessStateEnum



class Solcot(BaseModel):
    consecutive           = models.CharField(max_length=255, blank=False, null=False, unique=True, error_messages={'unique': 'Ya existe un solcot con este consecutivo'})
    product               = models.CharField(max_length=255, blank=False, null=False)
    quantity              = models.FloatField(blank=False, null=False)
    measurementUnit       = models.CharField(max_length=255, blank=False, null=False)
    budget                = models.FloatField(blank=False, null=False)
    solcot_type           = models.ForeignKey('request.solcotType', on_delete=models.CASCADE)
    specification         = models.TextField(blank=True, null=True)
    description           = models.TextField(blank=True, null=True)
    limit_date            = models.DateTimeField(blank=False, null=False)
    is_unique_provider    = models.BooleanField(default=False)
    is_visit_required     = models.BooleanField(default=False)
    contract_manager      = models.CharField(max_length=255, blank=False, null=False)
    solpet_code           = models.CharField(max_length=255, blank=True, null=True)
    global_administration = models.FloatField(blank=True, null=True)
    global_utility        = models.FloatField(blank=True, null=True)
    global_contingencies  = models.FloatField(blank=True, null=True)
    is_viewed_by_buyer    = models.BooleanField(default=False)
    accepted_at           = models.DateTimeField(blank=True, null=True)
    finished_at           = models.DateTimeField(blank=True, null=True)
    process_state         = models.CharField(max_length=255, choices=ProcessStateEnum.choices(), default=ProcessStateEnum.PENDING.value)
    shopping_group        = models.ForeignKey('request.shoppingGroup', on_delete=models.CASCADE)
    category              = models.ForeignKey('misc.category', on_delete=models.CASCADE)
    sub_category          = models.ForeignKey('misc.subCategory', on_delete=models.CASCADE)
    buyer                 = models.ForeignKey('authentication.users', on_delete=models.CASCADE, related_name='solcot_buyer')
    purchase_organization = models.ForeignKey('request.purchaseOrganization', on_delete=models.CASCADE)
    supra_solcot          = models.ForeignKey('request.supraSolcot', on_delete=models.CASCADE)
    logistic_center       = models.ForeignKey('request.logisticCenter', on_delete=models.CASCADE)

    class Meta:
        db_table            = 'solcot'
        verbose_name        = 'solcot'
        verbose_name_plural = 'solcot'


class SolcotLog(BaseLog):
    solcot = models.ForeignKey(Solcot, on_delete=models.CASCADE)

    class Meta:
        db_table            = 'solcot_log'
        verbose_name        = 'solcot_log'
        verbose_name_plural = 'solcot_log'

    