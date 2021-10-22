from django.contrib import admin

# Register your models here.
admin.site.site_header = 'KonwGoods管理后台'  # 设置header
admin.site.site_title = 'KonwGoods管理后台'  # 设置title
admin.site.index_title = 'KonwGoods管理后台'
from applet import models
from simpleui.admin import AjaxAdmin
@admin.register(models.user)
class user(admin.ModelAdmin):
    """
    后台user展示表
    """
    list_display = (
        'user_openid','username','sex','country','province',
        'city','language','user_level','user_point',
        'user_balance','user_createtime','user_isactive'
    )
    # 默认不配置的话，第一个字段会存在链接到记录编辑页面
    # list_display_links = None
    list_display_links = ('user_openid',)
    # 每页显示条目数 缺省值100
    list_per_page = 10
    # 设置过滤选项
    list_filter = ('user_openid','sex','province','user_level','user_isactive')
    # 按发布日期降序排序
    ordering = ('-user_createtime',)
    # 搜索条件设置
    search_fields = ('username',)

@admin.register(models.navar)
class navar(admin.ModelAdmin):
    """
    后台navar展示表
    """
    list_display = (
        'id','navar_name','seq',
    )
    list_display_links = ('id',)
    list_per_page = 10
    # 可编辑字段
    list_editable = ('navar_name','seq')
    ordering = ('seq',)
    search_fields = ('id',)

@admin.register(models.slideshow)
class slideshow(admin.ModelAdmin):
    """
    后台slideshow展示表
    """
    list_display = (
        'id', 'banner_name', 'is_show'
    )
    list_display_links = ('id',)
    list_per_page = 10
    list_editable =('banner_name','is_show',)
    ordering = ('id',)
    search_fields = ('id',)


@admin.register(models.productsale)
class productsale(admin.ModelAdmin):
    """
    后台productsale展示表
    """
    list_display = (
        'id', 'name', 'type','remark',
    )
    list_display_links = ('id',)
    list_filter = ('name','type',)
    list_editable = ('name', 'type','remark')
    list_per_page = 10
    ordering = ('id',)
    search_fields = ('id',)


@admin.register(models.productgoods)
class productgoods(admin.ModelAdmin):
    """
    后台productgoods展示表
    """
    # 设置页面可以展示的字段
    list_display =(
        'id','name','price','privilegePrice','discount','create_time',
        'goods_type','is_putaway'
    )
    list_display_links = ('id',)
    # 设置过滤选项
    list_filter = ('name','price','goods_type','is_putaway')
    list_per_page = 10
    list_editable = ('name','price','privilegePrice','discount','goods_type','is_putaway')
    # 按发布日期降序排序
    ordering = ('-create_time',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.productgoodsdetail)
class productgoodsdetail(admin.ModelAdmin):
    """
    后台productgoodsdetail展示表
    """
    list_display = (
        'id', 'title', 'stock_quantity', 'characteristic'
    )
    list_display_links = ('id',)
    list_filter = ( 'title', 'stock_quantity',)
    list_per_page = 10
    list_editable =('title', 'stock_quantity', 'characteristic')
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id', )

@admin.register(models.productgoodsdetail_slideshow)
class productgoodsdetail_slideshow(admin.ModelAdmin):
    list_display = (
        'id', 'detail_slideshow', 'productgoods',
    )
    list_display_links = ('id',)
    list_filter = ('productgoods',)
    list_per_page = 10
    list_editable = ( 'detail_slideshow', 'productgoods')
    # 按发布日期降序排序
    ordering = ('-id',)
    # 搜索条件设置
    search_fields = ('id',)

@admin.register(models.productgoodsdetail_img)
class productgoodsdetail_img(admin.ModelAdmin):
    """
    后台productgoodsdetail_img展示表
    """
    list_display = (
        'id', 'detail_img', 'productgoods',
    )
    list_display_links = ('id',)
    list_filter = ('productgoods',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)

@admin.register(models.good_category)
class good_category(admin.ModelAdmin):
    """
    后台good_category展示表
    """
    list_display = (
        'id', 'name',
    )
    list_display_links = ('id',)
    list_filter = ('name',)
    list_editable = ('name',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.good_categorychild)
class good_categorychild(admin.ModelAdmin):
    """
    后台good_categorychild展示表
    """
    list_display = (
        'id', 'name', 'img_url','category'
    )
    list_display_links = ('id',)
    list_filter = ('name', 'category',)
    list_editable = ('name',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)


@admin.register(models.goodcart)
class goodcart(admin.ModelAdmin):
    """
    后台goodcart展示表
    """
    list_display = (
        'id', 'productgood', 'productgood_num', 'user','goodtocart_time',
    )
    list_display_links = ('id',)
    list_filter = ('productgood', 'user','goodtocart_time',)
    # list_editable = ('name',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)

@admin.register(models.order)
class order(admin.ModelAdmin):
    """
    后台order展示表
    """
    list_display = (
        'order_id', 'order_title', 'user', 'productgoods', 'pay_price',
        'buy_number','order_status','pay_type','trade_no','order_status',
        'order_createtime','order_paytime','order_finishtime','order_addr',
        'oredr_detail','is_delete'
    )
    list_display_links = ('order_id',)
    list_filter = ('productgoods', 'user', 'order_status','pay_price','is_delete','order_createtime','order_paytime')
    list_editable = ('order_title',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('-order_createtime',)
    # 搜索条件设置
    search_fields = ('id','order_title')

@admin.register(models.order_detail)
class order_detail(admin.ModelAdmin):
    """
    后台order_detail展示表
    """
    list_display = (
        'id', 'logistics_company', 'logistics_number', 'is_free_freight', 'freight',
    )
    list_display_links = ('id',)
    list_filter = ('logistics_company', 'is_free_freight',)
    list_editable = ('is_free_freight',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id','logistics_number')


@admin.register(models.address)
class address(admin.ModelAdmin):
    """
    后台address展示表
    """
    list_display = (
        'id', 'consignee', 'mobile', 'user', 'address','transportDay','is_default',
    )
    list_display_links = ('id',)
    list_filter = ('transportDay', 'user', 'address',)
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)


from . import models
@admin.register(models.UserInfo)
class UserInfo(admin.ModelAdmin):
    """
    后台用户展示表
    """
    list_display = (
        'id', 'username', 'email', 'phone_code', 'is_staff', 'is_active', 'is_superuser','last_login',
    )
    list_display_links = ('id',)
    list_filter = ('username', 'email', 'is_superuser','is_active')
    list_per_page = 10
    # 按发布日期降序排序
    ordering = ('id',)
    # 搜索条件设置
    search_fields = ('id',)
