# 重写返回数据
from applet import serializers
def custom_jwt_response_payload_handler(token, user, request):
    return {
        'token': token,
        # 将user对象进行序列化
        'userinfo':serializers.UserModelSerializer(instance=user).data
    }
