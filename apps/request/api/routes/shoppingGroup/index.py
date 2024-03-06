# views
from django.urls import path
from apps.request.api.views.shoppingGroup.index  import ShoppingGroupAV

urlpatterns = [
    path('shoppingGroup', ShoppingGroupAV.as_view(), name='shoppingGroup'),
    path('shoppingGroup/<str:pk>', ShoppingGroupAV.as_view(), name='shoppingGroup_id')
]