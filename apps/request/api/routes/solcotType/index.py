# views
from django.urls import path
from apps.request.api.views.solcotType.index  import SolcotTypeAV

urlpatterns = [
    path('solcotType', SolcotTypeAV.as_view(), name='solcotType'),
    path('solcotType/<str:pk>', SolcotTypeAV.as_view(), name='solcotType_id')
]