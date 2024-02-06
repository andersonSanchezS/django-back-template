# views
from django.urls import path
from apps.authentication.api.views.role.index  import RoleAV

urlpatterns = [
    path('role', RoleAV.as_view(), name='role'),
    path('role/<str:pk>', RoleAV.as_view(), name='role_id')
]