from celery import Celery

broker = 'redis://127.0.0.1:6379/10'  # 消息队列缓存库
backend = 'redis://127.0.0.1:6379/11'  # 任务结果缓存库
# 由于celery和django 是独立的两个服务，要想在celery服务中使用django，必须加这两句
# 类似于在在其他非django内部的py文件中使用django，或者是app中的test文件引入一样
import os

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
        'task': 'celery_task.async_task.update_banner',  # 定时更新轮播图任务
        'schedule': timedelta(days=3),
    },
    'update_productsale_every_3_days': {
        'task': 'celery_task.async_task.update_productsale',  # 定时新品特卖任务
        'schedule': timedelta(days=3),
    },

}
