# Rest Framework
from rest_framework.generics import GenericAPIView
from django.db.models import Q
# Models
from apps.authentication.models import Users
# Utils
from apps.base.utils.index import response
import environ
import bcrypt
from datetime import timedelta, datetime as dt
import jwt


class LoginAV(GenericAPIView):
    # Initialise environment variables
    env = environ.Env()
    environ.Env.read_env()

    def post(self, request):
        try:
            # check if the user exists by his username or password
            user = Users.objects.filter(Q(username=request.data['username']) | Q(email=request.data['username'])).first()
            if user:
                # check if the user is active
                if user.state == 0:
                    return response.failed('Usuario inactivo')
                # check if the password is correct
                checkPassword = bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password[2:-1].encode('utf-8'))
                
                if checkPassword == False:
                    return response.failed('Usuario o contraseña incorrectos')
                
                if user.is_superuser:
                    payload = {
                    'id'              : user.id,
                    'first_name'      : user.first_name if user.first_name else '',
                    'last_name'       : user.last_name if user.last_name else '',
                    'role'            : None,
                    'email'           : user.email if user.email else '',
                    'is_superuser'    : user.is_superuser,
                    'exp'             : dt.utcnow() + timedelta(days=30)
                }

                # Generate the token
                token = jwt.encode(payload=payload, key=self.env('SECRET_KEY'), algorithm='HS256')
                # Check token
                # Create token
                return response.success('Inicio de sesión exitoso', { 'token': token, 'data': payload })
            else:
                return response.failed('Usuario y/o contraseña incorrectos')    
        except Exception as e:
            return response.failed(e.message, 500)