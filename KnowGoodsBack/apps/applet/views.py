# Create your views here.
from rest_framework.views import APIView
from utils.utils_app.APIresponse import APIResponse
from utils.utils_app.wxlogin import get_openid
from rest_framework.viewsets import ViewSet, GenericViewSet
from . import models
from . import serializers
from django.conf import settings
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from utils.utils_app.custom_jwt_response_payload_handler import custom_jwt_response_payload_handler


class Get_code(APIView):
    """
    根据前端传入的code,调用get_wxlogin_info得到session_key,openid对其进行加密并返回
    """

    def post(self, request):
        global openid
        openid, session_key = get_openid(request)
        if not (openid, session_key):
            return APIResponse(code=102, msg='未获取到openid,请稍后重试')
        print(openid)
        print(session_key)
        return APIResponse(openid=openid)


class Get_userdetail(APIView):
    """
    将用户详情数据存入用户表，并把openid也存入表中
    逻辑：
        判断数据库中此openid是否存在，
        存在就返回其数据并用rest_frameworkjwt进行加密
        不存在就创建此用户
        讲openid作为key，token作为value存入redis
    :return: 返回用户详情的数据
    """

    def post(self, request):

        userinfo = request.data.get('userInfo')
        open_id = request.META.get('HTTP_OPENID')
        if not userinfo:
            return APIResponse(code=103, msg='未获取到用户详情信息,请稍后重试')
        user_obj = models.user.objects.filter(user_openid=open_id).first()
        if not user_obj:
            nick_name = userinfo.get('nickName')
            sex = userinfo.get('gender')
            country = userinfo.get('country')
            province = userinfo.get('province')
            city = userinfo.get('city')
            language = userinfo.get('language')
            headingurl = userinfo.get('avatarUrl')
            user_obj = models.user.objects.create(
                user_openid=open_id,
                username=nick_name,
                sex=sex,
                country=country,
                province=province,
                city=city,
                language=language,
                headingurl=headingurl,
                user_level=1
            )
        if user_obj.user_isactive is False:
            return APIResponse(code=1001, msg='账户未激活，请联系管理员激活')
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        # 自定义返回token和其他数据
        response = custom_jwt_response_payload_handler(token, user_obj, request)
        # 将此用户的open_id和token存入缓存
        cache.set(settings.APPLET_CACHE_NAME % open_id, token)
        return APIResponse(result=response)


from rest_framework.generics import GenericAPIView
from django.core.cache import cache


class Rt_navbars(GenericAPIView):
    """
    返回导航栏名称
    """
    queryset = models.navar.objects.all().order_by('seq')
    serializer_class = serializers.NavbarsModelSerializer

    def get(self, request, *args, **kwargs):
        cache_Navabar = cache.get('导航栏缓存')
        if not cache_Navabar:
            res = self.get_queryset()
            serializer = self.get_serializer(instance=res, many=True)
            cache_Navabar = serializer.data
            cache.set('导航栏缓存', cache_Navabar)
        return APIResponse(result=cache_Navabar)


class Rt_banners(GenericAPIView):
    """
    返回轮播图接口
    """
    queryset = models.slideshow.objects.all()[:settings.BANNER_NUMBER]
    serializer_class = serializers.BannersModelSerializer

    def get(self, request):
        cache_Banners = cache.get('轮播图缓存')
        if not cache_Banners:
            res = self.get_queryset()
            serializer = self.get_serializer(instance=res, many=True)
            cache_Banners = serializer.data
            cache.set('轮播图缓存', cache_Banners)
        return APIResponse(result=cache_Banners)


class Rt_productsale(GenericAPIView):
    """
    获取新品特卖的接口
    """
    queryset = models.productsale.objects.all()[:settings.PRODUCTSALE_NUMBER]
    serializer_class = serializers.ProductsaleModelSerializer

    def get(self, request):
        cache_Productsale = cache.get('新品特卖缓存')
        if not cache_Productsale:
            res = self.get_queryset()
            serializer = self.get_serializer(instance=res, many=True)
            cache_Productsale = serializer.data
            cache.set('新品特卖缓存', cache_Productsale)
        return APIResponse(result=cache_Productsale)


from . import page


class Rt_pecialbenefits(APIView):
    """
    福利专场接口
    继承APIView实现分页
    """

    def get(self, request):
        # 反转queryset对象
        cache_productgoods = cache.get('福利专场缓存')
        if not cache_productgoods:
            all_productgoods = models.productgoods.objects.filter(is_putaway=True).all()[::-1]
            cache.set('福利专场缓存', all_productgoods)
            productgoodsPage = page.productgoodsPageNumber()
            res = productgoodsPage.paginate_queryset(all_productgoods, request, self)
            serializer = serializers.PecialbenefitsModelSerializer(instance=res, many=True)
            # 继承了PageNumberPagination重写了get_paginated_response
            return productgoodsPage.get_paginated_response(serializer.data)
        else:
            productgoodsPage = page.productgoodsPageNumber()
            res = productgoodsPage.paginate_queryset(cache_productgoods, request, self)
            serializer = serializers.PecialbenefitsModelSerializer(instance=res, many=True)
            # 继承了PageNumberPagination重写了get_paginated_response
            return productgoodsPage.get_paginated_response(serializer.data)

class Rt_gooddetail(ViewSet):
    """
    商品详情页接口
    """

    def retrieve(self, request):
        goodsId = request.query_params.get('goodsId')
        # 获取并序列化商品详情信息
        gooddetail_obj = models.productgoods.objects.filter(id=goodsId).first()
        res_detail = serializers.PecialbenefitsModelSerializer(instance=gooddetail_obj)
        # 获取并序列化轮播图片信息
        detailslideshow_obj = models.productgoodsdetail_slideshow.objects.filter(productgoods=goodsId).all()
        res_detailslideshow = serializers.GoodsdetailslideshowModelSerializer(instance=detailslideshow_obj, many=True)
        # 获取并序列化商品详情图片信息
        detailimg_obj = models.productgoodsdetail_img.objects.filter(productgoods=goodsId).all()
        res_detailimg = serializers.GoodsdetailimgModelSerializer(instance=detailimg_obj, many=True)
        return APIResponse(detail=res_detail.data, slideshow=res_detailslideshow.data, detailimg=res_detailimg.data)


class Rt_category(APIView):
    """
    主分类接口
    """

    def get(self, request):
        cache_Category = cache.get('主分类缓存')
        if not cache_Category:
            obj = models.good_category.objects.all()
            serializer = serializers.GoodcategoryModelSerializer(instance=obj, many=True)
            cache_Category = serializer.data
            cache.set('主分类缓存', cache_Category)
        return APIResponse(result=cache_Category)


class Rt_categoryindex(ViewSet):
    """
    二级分类接口
    """

    def list(self, request):
        index_id = request.query_params.get('indexId')
        cache_Categoryindex = cache.get('二级分类缓存id_%s' % index_id)
        if not cache_Categoryindex:
            obj = models.good_categorychild.objects.filter(category=index_id).all()
            serializer = serializers.GoodcategorychildModelSerializer(instance=obj, many=True)
            cache_Categoryindex = serializer.data
            cache.set('二级分类缓存id_%s' % index_id, cache_Categoryindex)
        return APIResponse(result=cache_Categoryindex)


class Rt_categorypreview(ViewSet):
    """
    分类页预览商品接口
    """

    def list(self, request):
        classify_id = request.query_params.get('classifyId')
        cache_Categorypreview = cache.get('分类页预览商品缓存id_%s' % classify_id)
        if not cache_Categorypreview:
            res = models.productgoods.objects.filter(categorychild=classify_id).all()
            serializer = serializers.PecialbenefitsModelSerializer(instance=res, many=True)
            cache_Categorypreview = serializer.data
            cache.set('分类页预览商品缓存id_%s' % classify_id, cache_Categorypreview)
        return APIResponse(result=cache_Categorypreview)


class Save_address(APIView):
    """
    保存用户地址接口
    """

    def post(self, request):
        print(request.data)
        token = request.data.get('token')
        openid = request.data.get('openid')
        # 取出此用户的token做对比
        cache_token = cache.get(settings.APPLET_CACHE_NAME % openid)
        if cache_token != token:
            return APIResponse(code=1002, msg='未携带token或缺少重要参数')
        address_obj = request.data.get('arr')
        if not address_obj:
            return APIResponse(code=1003, msg='缺少地址参数')
        consignee = address_obj.get('consignee')
        mobile = address_obj.get('mobile')
        address = address_obj.get('address')
        transportDay = address_obj.get('transportDay')
        user_obj = models.user.objects.filter(user_openid=openid).first()
        new_address_obj = models.address.objects.create(consignee=consignee, mobile=mobile,
                                                        address=address, transportDay=transportDay, user=user_obj)
        # 将地址对象进行序列化
        serializer = serializers.AddressModelSerializer(instance=new_address_obj)
        print(serializer.data)
        return APIResponse(result=serializer.data)


from utils.custom_check_jwt_authenticate import Applet_CUSTOMWebTokenAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import CreateAPIView, DestroyAPIView
from utils.knowGoods_logging import get_logger
from rest_framework.response import Response

logger = get_logger()


class AddCartGoodView(CreateAPIView):
    """
    商品添加购物车，写入数据库
    均记录到日志
    前端传入数据格式 :
                {
                "productgood":"商品id",
                "productgood_num":"添加到购物车中的商品数量",
                "user":"关联用户"
                }
    """
    authentication_classes = [Applet_CUSTOMWebTokenAuthentication, ]
    serializer_class = serializers.AddCartGoodModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return APIResponse(msg='加入购物车成功！')


class DelCartGoodView(DestroyAPIView):
    """
    商品从购物车中移除，删除数据库的此条数据
    均记录到日志
    """
    authentication_classes = [Applet_CUSTOMWebTokenAuthentication, ]

    def delete(self, request, *args, **kwargs):
        productgood = request.query_params.get('productgood')
        user_openid = request.META.get('HTTP_OPENID')
        instance = models.goodcart.objects.filter(productgood_id=productgood).first()
        self.perform_destroy(instance)
        logger.warning('用户:%s,已将商品(id):%s,从购物车中移除' % (user_openid,
                                                      productgood))
        return APIResponse(msg='删除成功！')

    def perform_destroy(self, instance):
        instance.delete()


class PayViewSet(GenericViewSet, CreateModelMixin):
    """
    商品购买与返回支付链接接口（已写好小程序token认证类）
    前端传入数据格式 :
            {
                "order_addr": "o407j4hdGv7JCSBGTDmupyKLlY2w",
                "pay_num":{"4541968687606792193":"2","4541970878803476481":"1"},
                "order_title": "TF口红",
                "pay_price": 1717
                }
    哪个user支付可以从请求头中获取
    均记录到日志
    """
    authentication_classes = [Applet_CUSTOMWebTokenAuthentication, ]
    serializer_class = serializers.PayModelModelSerializer

    def create(self, request, *args, **kwargs):
        pay_num = request.data.pop('pay_num')
        order_addr = request.data.pop('order_addr')
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request, 'pay_num': pay_num, 'order_addr': order_addr})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        pay_url = serializer.context.get('pay_url')
        return APIResponse(pay_url=pay_url)


import datetime


def Post_Pay_success(request):
    # 支付宝post回调，内网测不了
    try:
        result_data = request.POST.dict()
        # 订单号，我们给的
        out_trade_no = result_data.get('out_trade_no')
        trade_no = result_data.get('trade_no')
        # 签名
        signature = result_data.pop('sign')
        from lib.iPay import alipay
        # sdk的验证签名方法
        result = alipay.verify(result_data, signature)
        if result and result_data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            # 完成订单修改：订单状态、流水号、支付时间
            models.order.objects.filter(order_id=out_trade_no).update(order_status=2, trade_no=trade_no,
                                                                      order_paytime=datetime.datetime.now())
            # 完成日志记录
            logger.warning('%s订单支付成功' % out_trade_no)
            return Response('success')
        else:
            logger.error('%s订单支付失败' % out_trade_no)
    except:
        pass
    return Response('failed')


from django.shortcuts import render


def Get_Pay_success(request):
    """
    支付完成后的get回调函数
    """
    out_trade_no = request.GET.get('out_trade_no')
    total_amount = request.GET.get('total_amount')
    return render(request, 'pay_success.html', locals())


from django_filters.rest_framework.backends import DjangoFilterBackend


class Order_listViewSet(GenericViewSet, page.CustomListModelMixin):
    """
    用户订单列表
    此处继承了自定义的CustomListModelMixin类:CustomListModelMixin重写了list方法
    """
    queryset = models.order.objects.all()
    authentication_classes = [Applet_CUSTOMWebTokenAuthentication]
    serializer_class = serializers.OrderlistModelSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['order_status', 'order_title']
