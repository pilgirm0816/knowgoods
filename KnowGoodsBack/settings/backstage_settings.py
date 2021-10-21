# pip install django-cors-headers 解决后台跨域问题

#跨域增加忽略
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'token',
)

# 指定simpleui默认的主题,指定一个文件名，相对路径就从simpleui的theme目录读取
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'

# 网站logo
# 线上
# SIMPLEUI_LOGO = 'http://8.130.49.128:8000/logo/logo.png'
# 本地
SIMPLEUI_LOGO = 'http://127.0.0.1:8000/logo/logo.png'

# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

# 隐藏首页的快捷操作和最近动作
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION = False

# 修改首页设置, 指向新创建的首页
# 线上
# SIMPLEUI_HOME_PAGE = 'http://8.130.49.128:8000/backstage/v1/api/home/'
# 本地
SIMPLEUI_HOME_PAGE = 'http://127.0.0.1:8000/backstage/v1/api/home/'
SIMPLEUI_HOME_TITLE = '首页'
