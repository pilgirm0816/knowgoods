# 自定义获取小程序的login
from settings import dev
import requests
from .APIresponse import APIResponse

def get_wxlogin_info(code):
    """
    根据小程序端的wx.login获取到code
    再去wx官方给的请求地址获取响应数据
    响应数据内包括: session_key,openid
    :param code:
    :return:port_response_json/False
    """
    port_wxurl = dev.code2Session.format(dev.AppID,dev.AppSecret,code)
    port_response = requests.get(port_wxurl)
    # print(type(port_response))  port_response是字符串需要将其转为字典
    port_response_json = port_response.json()
    if port_response_json.get('errcode'):
        return False
    return port_response_json


# 对获取openid进行封装
def get_openid(request):
    param = request.data
    code = param.get('code')
    # 获取session_key,openid
    param_openid = get_wxlogin_info(code)
    if param_openid is False:
        return APIResponse(code=101, msg='获取信息失败,请稍后重试')

    openid = param_openid.get('openid')
    session_key = param_openid.get('session_key')

    return openid,session_key
