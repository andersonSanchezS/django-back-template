# views
from django.urls import path
from apps.authentication.api.views.menu.index  import MenuAV

urlpatterns = [
    path('menu', MenuAV.as_view(), name='menu'),
    path('menu/<str:pk>', MenuAV.as_view(), name='menu_id')
]