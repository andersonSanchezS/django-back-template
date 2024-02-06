# views
from django.urls import path
from apps.authentication.api.views.permission.index  import PermissionAV

urlpatterns = [
    path('permission', PermissionAV.as_view(), name='permission'),
    path('permission/<str:pk>', PermissionAV.as_view(), name='permission_id')
]