from .celery import app
from applet import models,serializers
from django.conf import settings

from django.core.cache import cache
# 定时更新轮播图函数
@app.task()
def update_banner():
    queryset = models.slideshow.objects.all()[:settings.BANNER_NUMBER]
    serializer = serializers.BannersModelSerializer(instance=queryset,many=True)
    cache_data = serializer.data
    cache.set('轮播图图片缓存', cache_data)
    return True


# 定时更新新品特卖函数
@app.task()
def update_productsale():
    queryset = models.productsale.objects.all()[:settings.PRODUCTSALE_NUMBER]
    serializer = serializers.ProductsaleModelSerializer(instance=queryset, many=True)
    cache_data = serializer.data
    cache.set('新品特卖图片缓存', cache_data)
    return True


# 定时更新福利专场函数
@app.task()
def update_pecialbenefits():
    all_productgoods = models.productgoods.objects.filter(is_putaway=True).all()[::-1]
    cache.set('福利专场缓存', all_productgoods)
    return True

# 定时任务（查询出数据库中所有付款后的商品在每六个小时之后，将待发货改为已发货同时生成订单详情，模拟物流）
@app.task()
def update_logistics_one():
    import random
    import uuid
    from django.db import transaction
    # 获取所有待发货的
    all_pending_obj = models.order.objects.filter(order_status=2).all()
    if not all_pending_obj:
        print(1)
    for pending_obj in all_pending_obj:
        freight = pending_obj.pay_price * 0.04
        res = random.randint(1, 5)
        if res == 1:
            logistics_number = 'jd' + str(uuid.uuid4())
            print(logistics_number)
        elif res == 2:
            logistics_number = 'sf' + str(uuid.uuid4())
        elif res == 3:
            logistics_number = 'yt' + str(uuid.uuid4())
        elif res == 4:
            logistics_number = 'st' + str(uuid.uuid4())
        else:
            logistics_number = 'bs' + str(uuid.uuid4())
        # 创建保存点
        save_id = transaction.savepoint()
        try:
            with transaction.atomic():
                # 写入订单详情
                order_detail_obj = models.order_detail.objects.create(
                    logistics_company=res,
                    logistics_number=logistics_number,
                    is_free_freight=False,
                    freight=freight
                )
                orderid = pending_obj.order_id
                models.order.objects.filter(order_id=orderid).update(order_status=3, oredr_detail=order_detail_obj)
        except:
            # 事务回滚
            transaction.savepoint_rollback(save_id)
        # 清除保存点
        transaction.clean_savepoints()


# 定时任务（查询出数据库中所有已发货的商品在每48个小时之后，将待发货改为已签收，模拟物流）
@app.task()
def update_logistics_two():
    models.order.objects.filter(order_status=3).update(order_status=4)
