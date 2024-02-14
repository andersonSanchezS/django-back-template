from django.contrib import admin
from django.urls    import path, include
from django.conf import settings

url = f'api/v{settings.API_VERSION}/'

urlpatterns = [
    # TODO: add a joke here 
    path('admin/', admin.site.urls),
    # Authentication
    path(f'{url}auth/', include('apps.authentication.api.routes.auth.index')),
    # Permissions
    path(f'{url}auth/', include('apps.authentication.api.routes.permission.index')),
    # Roles
    path(f'{url}auth/', include('apps.authentication.api.routes.role.index')),
    # Users
    path(f'{url}auth/', include('apps.authentication.api.routes.user.index')),
    # Misc
    path(f'{url}misc/', include('apps.misc.api.routes.typeDocument.index')),
]
