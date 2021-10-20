from .celery import app
from applet import models,serializers
from django.conf import settings
from django_redis import get_redis_connection
# 定时更新轮播图函数
@app.task()
def update_banner():
    queryset = models.slideshow.objects.all()[:settings.BANNER_NUMBER]
    serializer = serializers.BannersModelSerializer(instance=queryset,many=True)
    cache_data = serializer.data
    conn = get_redis_connection()
    conn.hset('轮播图图片缓存', 'Banners', cache_data)
    return True


# 定时更新新品特卖函数
@app.task()
def update_productsale():
    queryset = models.productsale.objects.all()[:settings.PRODUCTSALE_NUMBER]
    serializer = serializers.ProductsaleModelSerializer(instance=queryset, many=True)
    cache_data = serializer.data
    conn = get_redis_connection()
    conn.hset('新品特卖图片缓存', 'Productsale', cache_data)
    return True
