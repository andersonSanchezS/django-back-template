# views
from django.urls import path
from apps.request.api.views.supraSolcot.index  import SupraSolcotAV

urlpatterns = [
    path('supraSolcot', SupraSolcotAV.as_view(), name='supraSolcot'),
    path('supraSolcot/<str:pk>', SupraSolcotAV.as_view(), name='supraSolcot_id')
]