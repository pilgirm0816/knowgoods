from celery import Celery

broker = 'redis://127.0.0.1:6379/9'  # 消息队列缓存库
backend = 'redis://127.0.0.1:6379/10'  # 任务结果缓存库
# 由于celery和django 是独立的两个服务，要想在celery服务中使用django，必须加这两句
# 类似于在在其他非django内部的py文件中使用django，或者是app中的test文件引入一样
import os

# 通过在服务器中添加环境变量中的值来区别到底是使用dev还是pro
identify = os.environ.get('WAY')
if identify == 1:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KnowGoodsBack.settings.pro")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KnowGoodsBack.settings.dev")


app = Celery(__name__, broker=broker, backend=backend, include=[
    'celery_task.home_task',
])

# 修改时区和etc
app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False

# 配置定时任务
from datetime import timedelta
from celery.schedules import crontab

app.conf.beat_schedule = {
    'update_banner_every_3_days': {
        'task': 'celery_task.home_task.update_banner',  # 每三天的早上10点定时更新轮播图任务
        'schedule': timedelta(hours=10,days=3),
    },
    'update_productsale_every_3_days': {
        'task': 'celery_task.home_task.update_productsale',  # 每三天的早上10点定时新品特卖任务
        'schedule': timedelta(hours=10,days=3),
    },
    'update_pecialbenefits_every_10_hours_oneday':{
        'task':'celery_task.home_task.update_pecialbenefits',  # 每天早上10点定时更新福利专场任务
        'schedule': timedelta(hours=10,days=1),
    },
    'update_logistics_every_6_hours':{
        # 查询出数据库中所有付款后的商品在每六个小时之后，将待发货改为已发货同时生成订单详情
        'task':'celery_task.home_task.update_logistics_one',
        'schedule': timedelta(hours=6),
    },
    'update_logistics_every_48_hours':{
        # 查询出数据库中所有付款后的商品在每六个小时之后，将待发货改为已发货同时生成订单详情
        'task':'celery_task.home_task.update_logistics_two',
        'schedule': timedelta(hours=48),
    }

}
