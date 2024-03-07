from django.contrib import admin
from django.urls    import path, include
from django.conf import settings

url = f'api/v{settings.API_VERSION}/'

urlpatterns = [
    # TODO: add a joke here 
    path('admin/', admin.site.urls),
    # Authentication
    
    # Login, refresh
    path(f'{url}auth/', include('apps.authentication.api.routes.auth.index')),
    # Permissions
    path(f'{url}auth/', include('apps.authentication.api.routes.permission.index')),
    # Roles
    path(f'{url}auth/', include('apps.authentication.api.routes.role.index')),
    # Menus
    path(f'{url}auth/', include('apps.authentication.api.routes.menu.index')),
    # Users
    path(f'{url}auth/', include('apps.authentication.api.routes.user.index')),


    # Misc

    # Type documents
    path(f'{url}misc/', include('apps.misc.api.routes.typeDocument.index')),
    # Categories
    path(f'{url}misc/', include('apps.misc.api.routes.category.index')),
    # Subcategories
    path(f'{url}misc/', include('apps.misc.api.routes.subCategory.index')),


    # Request

    # Purchase organizations
    path(f'{url}request/', include('apps.request.api.routes.purchaseOrganization.index')),
    # Logistic centers
    path(f'{url}request/', include('apps.request.api.routes.logisticCenter.index')),
    # Shopping groups
    path(f'{url}request/', include('apps.request.api.routes.shoppingGroup.index')),
    # Cost centers
    path(f'{url}request/', include('apps.request.api.routes.costCenter.index')),
    # Solcot types
    path(f'{url}request/', include('apps.request.api.routes.solcotType.index')),
    # Taxes
    path(f'{url}request/', include('apps.request.api.routes.tax.index')),
    # Supra solcot
    path(f'{url}request/', include('apps.request.api.routes.supraSolcot.index')),
]
