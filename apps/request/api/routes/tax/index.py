# views
from django.urls import path
from apps.request.api.views.tax.index  import TaxAV

urlpatterns = [
    path('tax', TaxAV.as_view(), name='tax'),
    path('tax/<str:pk>', TaxAV.as_view(), name='tax_id')
]