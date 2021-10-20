from rest_framework import serializers
from . import models
from rest_framework.authentication import authenticate
from rest_framework.validators import ValidationError
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler


# 登录反序列化类
class LoginModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = models.UserInfo
        fields = ['username','password']
        # extra_kwargs = {
        #     'username': {'write_only': True},
        #     'password': {'write_only': True},
        # }


    def validate(self, attrs):
        """
        对前端传入的用户名密码进行校对
        比对成功返回token
        失败则直接抛异常
        """
        print(attrs)
        request = self.context.get('request')
        user = self._proofread_user(attrs,request)
        token = self._produce_token(user)
        self.context['token'] = token
        return attrs

    def _proofread_user(self,attrs,request):
        user = authenticate(request,username=attrs.get('username'),password=attrs.get('password'))
        print(user)
        if user is None:
            raise ValidationError({'detail':'账号密码有误'})

        return user

    def _produce_token(self,user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token
