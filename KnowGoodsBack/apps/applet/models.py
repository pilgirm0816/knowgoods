"""小程序端的数据表"""
from django.db import models


# Create your models here.


class user(models.Model):
    """
    KnowGoods 小程序端用户表不使用内置表
    """
    user_openid = models.CharField(max_length=128, verbose_name='唯一标识', primary_key=True)
    username = models.CharField(max_length=128, verbose_name='昵称')
    sex = models.IntegerField(verbose_name='性别', help_text='值为1时是男性，为2时是女性，0是未知')
    country = models.CharField(max_length=64, verbose_name='国家')
    province = models.CharField(max_length=64, verbose_name='省份')
    city = models.CharField(max_length=64, verbose_name='城市')
    language = models.CharField(max_length=32, verbose_name='语言')
    headingurl = models.TextField(verbose_name='头像地址')
    level_type = (
        (1, '普通会员'),
        (2, '白银会员'),
        (3, '黄金会员'),
        (4, '砖石会员')
    )
    user_level = models.SmallIntegerField(choices=level_type, verbose_name='会员等级')
    user_point = models.IntegerField(verbose_name='积分', default=0)
    user_balance = models.FloatField(default=0, verbose_name='余额')
    user_createtime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    user_isactive = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        verbose_name = '小程序端用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_openid

    def user_level_name(self):
        return self.get_user_level_display()


class navar(models.Model):
    """
    首页导航栏表
    """
    navar_name = models.CharField(max_length=32, verbose_name='名称')
    seq = models.IntegerField(verbose_name='顺序')

    class Meta:
        verbose_name = '首页导航栏'
        verbose_name_plural = verbose_name


class slideshow(models.Model):
    """
    首页轮播图表
    """
    banner_name = models.CharField(max_length=128, verbose_name='名称')
    img_url = models.TextField(verbose_name='图片路径')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    click_url = models.CharField(max_length=256, verbose_name='点击链接')

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name


class productsale(models.Model):
    """
    新品特卖表
    """
    name = models.CharField(max_length=128, verbose_name='名称')
    img_url = models.CharField(max_length=128, verbose_name='图片地址')
    type = models.CharField(max_length=32, verbose_name='类型', default='temai')
    remark = models.CharField(max_length=64, verbose_name='描述')

    class Meta:
        verbose_name = '新品特卖'
        verbose_name_plural = verbose_name


class productgoods(models.Model):
    """
    商品表
    商品id通过雪花算法来实现
    雪花算法是一款基于tornado框架实现的
    在终端中执行以下命令:snowflake_start_server
    在8910端口开启服务
    详情用法见utils.utils_app.snow_flake的get_snowflake_uuid与scripts下的snowflake.py文件
    """
    id = models.CharField(unique=True, verbose_name='编号', primary_key=True, max_length=128)
    name = models.CharField(max_length=32, verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='入库时间')
    show_img = models.CharField(max_length=256, verbose_name='展示图片路径')
    price = models.FloatField(verbose_name='现价格')
    privilegePrice = models.FloatField(verbose_name='原价格')
    discount = models.FloatField(verbose_name='折扣', default=7)
    detail = models.OneToOneField(to='productgoodsdetail', on_delete=models.DO_NOTHING, verbose_name='详情信息')
    categorychild = models.ForeignKey(to='good_categorychild', on_delete=models.CASCADE, verbose_name='所属子分类',
                                      null=True)
    show_video = models.CharField(max_length=256, verbose_name='有关视频')
    type = (
        (1, '电脑办公'),
        (2, '手机'),
        (3, '运动户外'),
        (4, '美妆护肤'),
        (5, '女装'),
    )
    goods_type = models.SmallIntegerField(choices=type, verbose_name='类型')
    is_putaway = models.BooleanField(default=True, verbose_name='是否上架')

    class Meta:
        verbose_name = '商品列表'
        verbose_name_plural = verbose_name

    @property
    def get_detail(self):
        return {'title': self.detail.title, 'stock': self.detail.stock_quantity}

    def goods_type_name(self):
        return self.get_goods_type_display()

class productgoodsdetail(models.Model):
    """
    商品详情信息
    """
    title = models.CharField(max_length=128, verbose_name='标题')
    stock_quantity = models.IntegerField(default=0, verbose_name='库存数量')
    characteristic = models.CharField(max_length=128, verbose_name='规格')

    class Meta:
        verbose_name = '商品详情'
        verbose_name_plural = verbose_name


class productgoodsdetail_slideshow(models.Model):
    """
    商品详情页轮播图片表
    """
    detail_slideshow = models.CharField(max_length=256, verbose_name='详情页轮播图')
    productgoods = models.ForeignKey(to=productgoods, on_delete=models.CASCADE, verbose_name='关联商品id',db_constraint=False)

    class Meta:
        verbose_name = '详情页轮播图片'
        verbose_name_plural = verbose_name


class productgoodsdetail_img(models.Model):
    """
    商品详情图片表
    """
    detail_img = models.CharField(max_length=256, verbose_name='详情页商品详情图片')
    productgoods = models.ForeignKey(to=productgoods, on_delete=models.CASCADE, verbose_name='关联商品id',db_constraint=False)

    class Meta:
        verbose_name = '详情页详情图片'
        verbose_name_plural = verbose_name


class good_category(models.Model):
    """
    商品分类表
    """
    name = models.CharField(max_length=16, verbose_name='商品分类名称')

    class Meta:
        verbose_name = '主分类'
        verbose_name_plural = verbose_name


class good_categorychild(models.Model):
    """
    商品分类小表
    """
    name = models.CharField(max_length=16, verbose_name='商品子分类名称')
    img_url = models.CharField(max_length=256, verbose_name='图片地址', null=True)
    category = models.ForeignKey(to=good_category, on_delete=models.DO_NOTHING, null=True, db_constraint=False,verbose_name='主分类id')

    class Meta:
        verbose_name = '子分类'
        verbose_name_plural = verbose_name


class goodcart(models.Model):
    """
    商品被添加到购物车表
    """
    productgood = models.ForeignKey(productgoods, related_name='goodcart', on_delete=models.DO_NOTHING,
                                    verbose_name='关联商品id')
    productgood_num = models.CharField(max_length=10, verbose_name='添加到购物车的商品数量')
    user = models.ForeignKey(user, on_delete=models.DO_NOTHING, verbose_name='关联用户id')
    goodtocart_time = models.DateTimeField(auto_now_add=True, verbose_name='添加的时间')
    class Meta:
        verbose_name = '用户购物车'
        verbose_name_plural = verbose_name

from django.utils.html import format_html
class order(models.Model):
    """
    商品订单信息表
    订单id通过uuid来实现
    """
    order_id = models.CharField(max_length=64, verbose_name='ID')
    order_title = models.CharField(max_length=150, verbose_name="标题", null=True)
    user = models.ForeignKey(to=user, on_delete=True, verbose_name='关联用户id')
    productgoods = models.ForeignKey(productgoods, on_delete=models.DO_NOTHING, null=True, verbose_name='关联商品id')
    pay_price = models.FloatField(verbose_name='支付金额')
    buy_number = models.IntegerField(verbose_name='购买数量', default=1)
    status_type = (
        (1, '待付款'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '已签收'),
        (5, '待评价'),
        (6, '已评价'),
    )
    trade_no = models.CharField(max_length=64, null=True, verbose_name="支付宝流水号")
    order_status = models.SmallIntegerField(choices=status_type, verbose_name='订单状态', default=1)
    order_createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    order_finishtime = models.DateTimeField(null=True, verbose_name='完成时间')
    pay_type = models.CharField(max_length=16, default='支付宝', verbose_name="支付方式")
    order_paytime = models.DateTimeField(null=True, verbose_name='支付时间')
    order_addr = models.ForeignKey(to='address', on_delete=models.DO_NOTHING, verbose_name='关联地址',
                                   db_constraint=False)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除',help_text='订单在用户层面是否删除')
    oredr_detail = models.OneToOneField('order_detail', on_delete=models.DO_NOTHING, null=True, verbose_name='订单外键')

    @property
    def get_productgoods(self):
        return {'productgoods_id':self.productgoods.id,
                'show_img':self.productgoods.show_img,
                'title':self.productgoods.name
                }
    def order_status_name(self):
        return self.get_order_status_display()

    # def colored_name(self):
    #     if self.order_status == '待付款':
    #         cl_name = 'red'
    #     return format_html(
    #         '<span style="color: {};">{}</span>',
    #         cl_name,
    #         self.order_status,
    #     )

    class Meta:
        verbose_name = '订单列表'
        verbose_name_plural = verbose_name


class order_detail(models.Model):
    """
    订单详情表
    """
    company_type = (
        (1, '京东'),
        (2, '顺丰'),
        (3, '圆通'),
        (4, '申通'),
        (5, '百世'),
    )
    logistics_company = models.SmallIntegerField(choices=company_type, null=True,verbose_name='物流公司')
    logistics_number = models.CharField(max_length=128, verbose_name='物流订单编号')
    is_free_freight = models.BooleanField(default=True, verbose_name='是否免除运费')
    freight = models.FloatField(default=0, verbose_name='订单运费')
    class Meta:
        verbose_name = '订单详情列表'
        verbose_name_plural = verbose_name

    def logistics_company_name(self):
        return self.get_logistics_company_display()

class address(models.Model):
    """
    用户地址表
    """
    consignee = models.CharField(max_length=64, verbose_name='收件人姓名')
    mobile = models.CharField(max_length=16, verbose_name='联系方式')
    address = models.CharField(max_length=256, verbose_name='地址')
    transportDay = models.CharField(max_length=64, verbose_name='收货时间', default='')
    is_default = models.BooleanField(default=True, verbose_name='是否为默认地址')
    user = models.ForeignKey(to=user, on_delete=True, verbose_name='关联用户', db_constraint=False)

    class Meta:
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
