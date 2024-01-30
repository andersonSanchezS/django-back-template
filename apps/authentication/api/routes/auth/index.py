# views
from django.urls import path
from apps.authentication.api.views.login.index  import LoginAV

urlpatterns = [
    path('login', LoginAV.as_view(), name='login'),
]