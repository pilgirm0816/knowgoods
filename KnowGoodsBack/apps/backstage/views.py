from django.shortcuts import render


from rest_framework.views import APIView

from applet import models
import datetime
from django.db.models import Avg, Max, Min, Sum, Count
from utils.utils_backstage import server_statistics


def home(request):
    """
    echarts图表数据
    """
    this_year = datetime.datetime.now().year
    this_month = datetime.datetime.now().month
    # 先年月筛选数据,然后以每天进行分组,格式化日期，将日期格式化成天数，再分组，统计每天的数据条数，输出
    week_order_statistics = models.order.objects.filter(order_createtime__year=this_year,
                                                        order_createtime__month=this_month, is_delete=False).extra(
        select={"order_createtime": "DATE_FORMAT(order_createtime,'%%e')"}).values('order_createtime').annotate(
        day_buy_number=Count("order_createtime")).values('order_createtime', 'day_buy_number')
    # 得到一周订单数的列表
    week_order_statistics_number = []
    # 由于数据量多的话需要对列表长度进行判断
    if len(week_order_statistics) > 5:
        new_week_order_statistics = week_order_statistics[-5:]
        for order_statistics in new_week_order_statistics:
            number = order_statistics.get('day_buy_number')
            new_week_order_statistics.append(number)
    for order_statistics in week_order_statistics:
        number = order_statistics.get('day_buy_number')
        week_order_statistics_number.append(number)

    # 进货量与出货量

    # 库存数量统计
    quantity_num = models.productgoods.objects.order_by('goods_type').values('goods_type', 'detail__stock_quantity')
    computer_office_quantity = 0
    phone_quantity = 0
    exercise_outdoors_quantity = 0
    SASA_quantity = 0
    women_wear_quantity = 0
    for i in quantity_num:
        if i.get('goods_type') == 1:
            computer_office_quantity += int(i.get('detail__stock_quantity'))
        elif i.get('goods_type') == 2:
            phone_quantity += int(i.get('detail__stock_quantity'))
        elif i.get('goods_type') == 3:
            exercise_outdoors_quantity += int(i.get('detail__stock_quantity'))
        elif i.get('goods_type') == 4:
            SASA_quantity += int(i.get('detail__stock_quantity'))
        else:
            women_wear_quantity += int(i.get('detail__stock_quantity'))
    # 获取cpu使用率
    cpu_info = server_statistics.get_cpu_info()
    return render(request, 'home.html', locals())
