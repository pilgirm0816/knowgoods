# 小程序ID
AppID = 'wx663a5bcec2342edb'
# 小程序密钥
AppSecret = '8ef3b2a99aae1c48b310e507d4ad877a'

# 登录凭证校验接口。通过 wx.login 接口获得临时登录凭证code得到session_key,openid
code2Session = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'


# 首页轮播图条数
BANNER_NUMBER = 4

# 新品特卖展示数量
PRODUCTSALE_NUMBER = 3

# 小程序用户缓存name
APPLET_CACHE_NAME = '小程序用户_%s'
