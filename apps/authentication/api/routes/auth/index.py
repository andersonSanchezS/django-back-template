# views
from django.urls import path
from apps.authentication.api.views.login.index  import LoginAV
from apps.authentication.api.views.refresh.index import RefreshAV

urlpatterns = [
    path('login', LoginAV.as_view(), name='login'),
    path('refresh', RefreshAV.as_view(), name='refresh'),
]