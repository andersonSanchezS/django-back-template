# views
from django.urls import path
from apps.request.api.views.costCenter.index  import CostCenterAV

urlpatterns = [
    path('costCenter', CostCenterAV.as_view(), name='costCenter'),
    path('costCenter/<str:pk>', CostCenterAV.as_view(), name='costCenter_id')
]