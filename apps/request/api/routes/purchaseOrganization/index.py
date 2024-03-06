# views
from django.urls import path
from apps.request.api.views.purchaseOrganization.index  import PurchaseOrganizationAV

urlpatterns = [
    path('purchaseOrganization', PurchaseOrganizationAV.as_view(), name='purchaseOrganization'),
    path('purchaseOrganization/<str:pk>', PurchaseOrganizationAV.as_view(), name='purchaseOrganization_id')
]