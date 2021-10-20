from rest_framework_jwt.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from rest_framework_jwt.utils import jwt_decode_handler
from applet import models

class Applet_CUSTOMWebTokenAuthentication(BaseAuthentication):
    """
    自定义小程序token,openid认证类
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        open_id = request.META.get('HTTP_OPENID')
        if not (token and open_id):
            raise exceptions.AuthenticationFailed({'detail':'未携带token和openid'})

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = {'detail':'签名已经过期'}
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = {'detail':'错误token签名'}
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = models.user.objects.filter(pk=open_id).first()

        return (user, token)


