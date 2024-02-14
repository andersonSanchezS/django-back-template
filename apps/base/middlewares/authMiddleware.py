# Rest framework
from django.http import JsonResponse
# Models 
from apps.authentication.models import Users
# Exceptions
from apps.base.exceptions import HTTPException
# Utils
import jwt
import time
import json
from django.conf import settings

class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # delete the bearer 
            token = request.headers.get('Authorization').split(' ')[1] if request.headers.get('Authorization') else None

            # if request path has auth/login, then continue with the normal flow
            checkPath = "auth/login" in request.path
            if checkPath:
                response = self.get_response(request)
                return response

            if not token:
                return JsonResponse({'error': True, 'message': 'No se ha proporcionado un token de autenticación.'}, status=401)

            # check if the token is valid
            try:
                checkToken = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except Exception as e:
                return JsonResponse({'error': True, 'message': 'El token proporcionado no es válido.'}, status=401)

            # check if the token is expired
            if checkToken['exp'] < int(time.time()):
                return JsonResponse({'error': True, 'message': 'El token proporcionado ha expirado.'}, status=401)

            # get the user from the request
            user = Users.objects.get(id=checkToken['id'])
            # check if the user is active
            if user.state == 0:
                return JsonResponse({'error': True, 'message': 'El usuario se encuentra inactivo.'}, status=401)
            
            # add the user to the request
            request._user = user

            # if the request has a body
            if not request.body:
                response = self.get_response(request)
                return response

            requestBody = json.loads(request.body.decode('utf-8'))
            # check if the request method is post put or patch
            if request.method == 'POST':
                # add the user to the request - user_created_at
                requestBody['user_created_at'] = user.id
                requestBody['user_updated_at'] = user.id
            elif request.method in ['PUT', 'PATCH']:
                # add the user to the request - user_updated_at
                requestBody['user_updated_at'] = user.id
            # new body length
            request.META['CONTENT_LENGTH'] = len(json.dumps(requestBody).encode('utf-8'))
            
            # update the body
            request._body = json.dumps(requestBody).encode('utf-8')

            response = self.get_response(request)
            return response
        except Exception as e:
            raise HTTPException(e.message, 500)