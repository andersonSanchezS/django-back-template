# Rest Framework
from rest_framework.generics import GenericAPIView
from django.db.models import Q
# Models
from apps.authentication.models import Users, Token
# Utils
from apps.base.utils.index import response
import bcrypt
from apps.authentication.utils.genjwt import genJwt
from django.conf import settings
# Ldap toolkit
from ldap3 import Server, Connection, ALL, SYNC


class LoginAV(GenericAPIView):
    
    def post(self, request):
        try:
            # check if the user exists by his username or password
            user = Users.objects.filter(Q(username=request.data['username']) | Q(email=request.data['username'])).first()
            if user:
                # check if the user is active
                if user.state == 0:
                    return response.failed('Usuario inactivo')
                
                if user.is_ldap_user:
                     # Connect to ldap server
                    server   = Server(settings.LDAP_HOST, port=int(settings.LDAP_PORT), get_info=ALL)
                    # Bind to ldap server
                    instance = Connection(server, version=3, auto_referrals=0, client_strategy=SYNC, lazy=False,
                                        user=user.email,password=request.data['password'])
                    bind = instance.bind()
                    # Check if the user credentials are correct
                    if bind == False:
                        return response.success({'error':True, 'message': 'Usuario y/o Contraseña incorrectos'}, 400)
                else:
                    # check if the password is correct
                    checkPassword = bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password[2:-1].encode('utf-8'))

                    if checkPassword == False:
                        return response.failed('Usuario o contraseña incorrectos')
                # gen tokens
                tokens = genJwt(user)
                return response.success('Inicio de sesión exitoso', { 'access_token': tokens['access_token'], 'refresh_token': tokens['refresh_token'] })
            else:
                return response.failed('Usuario y/o contraseña incorrectos')    
        except Exception as e:
            return response.failed(str(e), 500)