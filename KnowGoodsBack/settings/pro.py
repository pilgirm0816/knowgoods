import os,sys
from .applet_settings import *
from .backstage_settings import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将BASE_DIR和apps加入环境变量
sys.path.insert(0,BASE_DIR)
sys.path.insert(1,os.path.join(BASE_DIR,'apps'))


# 密钥
SECRET_KEY = 'ge(b7=%j%0&07iyif*hz-a2hken3in5_@-q71p^!tnt!u#u8w9'

# 上线改为False
DEBUG = False
# 可以访问的ip
ALLOWED_HOSTS = ['*']




INSTALLED_APPS = [
    'simpleui',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'applet',
    'backstage',
    'rest_framework',
    'django_filters'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'KnowGoodsBack.urls'

# 由于更改了BASE_DIR，templates位置的路径也需要更改
TEMPLATES_PATH = os.path.dirname(BASE_DIR)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(TEMPLATES_PATH,'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'KnowGoodsBack.wsgi.application'



# 采用mysql数据库
# 数据库密码存放在环境变量中
PASSWORD = os.environ.get('PASSWORD','Zbin1234?')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'knowgoods',
        'USER': 'root',
        'PASSWORD': 'Zbin1234?',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CHARSET': 'utf8'
    }
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# 做国际化处理
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False


AUTH_USER_MODEL ='backstage.UserInfo'

STATIC_URL = '/static/'
# 使用simple将静态文件复制到static下
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
STATICFILES_DIRS = [
     os.path.join(os.path.dirname(BASE_DIR), "static"),
 ]
# 开启media路径
LOGO_ROOT = os.path.join(os.path.dirname(BASE_DIR),'logo' )  # 开启的路径
LOGO_URL = '/logo/'  # 访问的路径


REST_FRAME = {
    'JWT_RESPONSE_PAYLOAD_HANDLER':'utils.utils_app.custom_jwt_response_payload_handler.custom_jwt_response_payload_handler'
}


# 真实项目上线后，日志文件打印级别不能过低，因为一次日志记录就是一次文件io操作
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 日志格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 过滤
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs", "knowGoods_all.log"),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'verbose',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs", "knowGoods_error.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 文件内容编码
            'encoding': 'utf-8'
        },
        'console': {
            # 实际开发建议使用WARNING
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'info': {
            # 实际开发建议使用ERROR
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR代表的是小knowGoods
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs", "knowGoods_info.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 文件内容编码
            'encoding': 'utf-8'
        },
    },
    # 日志对象
    'loggers': {
        'knowGoods': {
            'handlers': ['console','info', 'default', 'error',],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}


# 使用redis作为缓存数据库
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/12",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 'decode_responses': True   添加这一行,数据正常返回，否则将以bytes返回
            "CONNECTION_POOL_KWARGS": {"max_connections": 100,}
            # "PASSWORD": "123",
        }
    }
}

import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=2),
}

# 上线后必须换成官网地址
# 同步回调的接口(get)，前后台分离时一般设置前台页面url
RETURN_URL = 'http://8.130.49.128:8000/applet/v1/api/pay/success/'
# 异步回调的接口(post)，一定设置为后台服务器接口
NOTIFY_URL = 'http://8.130.49.128:8000/order/success/'


REST_FRAMEWORK = {
   # 过滤器默认后端
    'DEFAULT_FILTER_BACKENDS': (
           'django_filters.rest_framework.DjangoFilterBackend',),
}
