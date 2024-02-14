# Utils
from apps.base.utils.index import response

# a decorator that checks if the user has the required role and/or permissions
def checkPermissions(roles=None,permissions=None):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            try:
                requestUser = args[0]._request._user
                
                if requestUser.is_superuser:
                    return function(request, *args, **kwargs)
                else:
                    # Get the user's roles and permissions
                    # check if the user has the required role
                    userRoles = set(role.description for role in requestUser.roles.all())
                    required_roles = set(roles)
                    if not required_roles.issubset(userRoles):
                         return response.failed({'error': 'No tiene los roles requeridos'}, 401)

                    # check if the user has the required permissions

                    # get all the permissions of the user
                    userPermissions = set(permission.description for role in requestUser.roles.all() for permission in role.permissions.all())
                    userPermissions.update(permission.description for permission in requestUser.custom_permissions.all())

                    required_permissions = set(permissions)  # 'permissions' debe ser una lista de descripciones de permisos requeridos
                    if not required_permissions.issubset(userPermissions):
                        return response.failed({'error': 'No tienes los permisos necesarios'}, 401)

                return function(request, *args, **kwargs)
            except Exception as e:
                return response.failed({'error': str(e)}, 500)
        return wrapper
    return decorator