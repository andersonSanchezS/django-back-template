# views
from django.urls import path
from apps.authentication.api.views.user.index  import UserAV

urlpatterns = [
    path('user', UserAV.as_view(), name='user'),
    path('user/<str:pk>', UserAV.as_view(), name='user_id')
]