from django.contrib import admin
from django.urls    import path, include
import environ

env = environ.Env()
environ.Env.read_env()


urlpatterns = [
    # TODO: add a joke here 
    path('admin/', admin.site.urls),
    # Authentication
    path(f'api/v{env("API_VERSION")}/auth/', include('apps.authentication.api.routes.auth.index')),
]
