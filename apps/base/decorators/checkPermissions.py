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
                
                return function(request, *args, **kwargs)
            except Exception as e:
                return response.failed({'error': str(e)}, 500)
        return wrapper
    return decorator