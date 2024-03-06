# views
from django.urls import path
from apps.request.api.views.logisticCenter.index  import LogisticCenterAV

urlpatterns = [
    path('logisticCenter', LogisticCenterAV.as_view(), name='logisticCenter'),
    path('logisticCenter/<str:pk>', LogisticCenterAV.as_view(), name='logisticCenter_id')
]