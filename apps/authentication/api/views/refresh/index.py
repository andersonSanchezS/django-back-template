# Rest Framework
from rest_framework.generics import GenericAPIView
# Models
from apps.authentication.models import Users, Token
# Utils
from apps.base.utils.index import response
import environ
import jwt
from apps.authentication.utils.genjwt import genJwt


class RefreshAV(GenericAPIView):
    # Initialise environment variables
    env = environ.Env()
    environ.Env.read_env()

    def post(self, request):
        try:
            # decode the token
            token = jwt.decode(request.data['refresh_token'], key=self.env('SECRET_KEY'), algorithms='HS256')
            
            # check if the user who is trying to refresh the token exists and it's the same as the token user
            getToken = Token.objects.get(id=token['token_id'])
            user = Users.objects.get(id=getToken.user.id)

            if  request._user.id != getToken.user.id:
                return response.failed('Token invalido', 401)
            # gen a new token
            tokens = genJwt(user)
            return response.success('Token refrescado', { 'access_token': tokens['access_token'], 'refresh_token':tokens['refresh_token'] })
        except Exception as e:
            return response.failed(str(e), 500)