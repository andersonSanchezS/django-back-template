# Models
from apps.authentication.models import Token

from datetime import timedelta, datetime as dt
import jwt
import ulid
import environ
from django.utils import timezone



def genJwt(user):
    try:
        environment = environ.Env()
        environment.read_env()

        payload = {
                'id'              : user.id,
                'first_name'      : user.first_name if user.first_name else '',
                'last_name'       : user.last_name if user.last_name else '',
                'role'            : None if user.is_superuser else [{'name': role.description} for role in user.roles.all()],
                'email'           : user.email if user.email else '',
                'is_superuser'    : user.is_superuser,
                'exp'             : timezone.make_aware(dt.utcnow() + timedelta(days=3))
            }

        # Generate the token
        token = jwt.encode(payload=payload, key=environment('SECRET_KEY'), algorithm='HS256')
        # Save token
        tokenInstance = Token.objects.create(id=ulid.new().str, token=token, user= user, is_valid= True, expiration= payload['exp'])
        # generate a refresh token
        refreshPayload = { 'token_id' : tokenInstance.id }
        refreshToken = jwt.encode(payload=refreshPayload, key=environment('SECRET_KEY'), algorithm='HS256')
        
        return {
            'access_token': token,
            'refresh_token': refreshToken
            }
    

    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
            }