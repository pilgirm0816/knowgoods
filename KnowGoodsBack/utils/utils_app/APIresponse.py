# 封装全局response响应
from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self, code=200, msg='成功',headers=None, exception=False,**kwargs):
        data = {'code': code, 'msg': msg}
        if kwargs:
            data.update(kwargs)
        super().__init__(data=data,headers=headers,exception=exception)


