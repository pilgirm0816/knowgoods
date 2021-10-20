# 序列化类
from rest_framework import serializers
from . import models
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from rest_framework.exceptions import ValidationError
from utils.knowGoods_logging import get_logger
logger = get_logger()

class UserModelSerializer(serializers.ModelSerializer):
    """
    获取用户序列化类
    """
    class Meta:
        model = models.user
        fields = ['user_openid','username','sex','headingurl','user_level','user_point','user_balance']
        extra_kwargs = {
            'user_openid':{'read_only':True},
            'username':{'read_only':True},
            'sex':{'read_only':True},
            'headingurl':{'read_only':True},
            'user_level':{'read_only':True},
            'user_point':{'read_only':True},
            'user_balance':{'read_only':True},
        }




class NavbarsModelSerializer(serializers.ModelSerializer):
    """
    导航条序列化类
    """
    class Meta:
        model = models.navar
        fields = ['id', 'navar_name', 'seq']
        extra_kwargs = {
            'id': {'read_only': True},
            'navar_name': {'read_only': True},
            'seq': {'read_only': True}
        }



class BannersModelSerializer(serializers.ModelSerializer):
    """
    轮播图序列化类
    """
    class Meta:
        model = models.slideshow
        fields = ['id', 'banner_name', 'img_url', 'is_show', 'click_url']
        extra_kwargs = {
            'id': {'read_only': True},
            'banner_name': {'read_only': True},
            'img_url': {'read_only': True},
            'is_show': {'read_only': True},
            'click_url': {'read_only': True}
        }



class ProductsaleModelSerializer(serializers.ModelSerializer):
    """
    新品特卖序列化类
    """
    class Meta:
        model = models.productsale
        fields = ['id', 'name', 'img_url', 'type', 'remark']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'img_url': {'read_only': True},
            'type': {'read_only': True},
            'remark': {'read_only': True}
        }



class PecialbenefitsModelSerializer(serializers.ModelSerializer):
    """
    福利专场序列化类
    """
    class Meta:
        model = models.productgoods
        fields = ['id', 'name', 'show_img', 'price', 'privilegePrice', 'get_detail', 'discount','show_video']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'show_img': {'read_only': True},
            'price': {'read_only': True},
            'privilegePrice': {'read_only': True},
            'get_detail': {'read_only': True},
            'discount': {'read_only': True},
            'show_video': {'read_only': True},
        }



class GoodsdetailslideshowModelSerializer(serializers.ModelSerializer):
    """
    商品详情页轮播图片序列化类
    """
    class Meta:
        model = models.productgoodsdetail_slideshow
        fields = ['detail_slideshow']
        extra_kwargs = {
            'detail_slideshow': {'read_only': True},
        }



class GoodsdetailimgModelSerializer(serializers.ModelSerializer):
    """
    商品详情图片序列化类
    """
    class Meta:
        model = models.productgoodsdetail_img
        fields = ['detail_img']
        extra_kwargs = {
            'detail_img': {'read_only': True},
        }



class GoodcategoryModelSerializer(serializers.ModelSerializer):
    """
    商品分类序列化类
    """
    class Meta:
        model = models.good_categorychild
        fields = ['id','name']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
        }


class GoodcategorychildModelSerializer(serializers.ModelSerializer):
    """
    商品分类子序列化类
    """
    class Meta:
        model = models.good_categorychild
        fields = ['id','name','img_url','category']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'read_only': True},
            'img_url': {'read_only': True},
            'category': {'read_only': True},
        }



class AddressModelSerializer(serializers.ModelSerializer):
    """
    地址序列化类
    """
    class Meta:
        model = models.address
        fields = ['consignee','mobile','address','transportDay','user']
        extra_kwargs = {
            'consignee': {'read_only': True},
            'mobile': {'read_only': True},
            'address': {'read_only': True},
            'transportDay': {'read_only': True},
            'user': {'read_only': True},
        }


class AddCartGoodModelSerializer(serializers.ModelSerializer):
    productgood = serializers.PrimaryKeyRelatedField(queryset=models.productgoods.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=models.user.objects.all())
    """
    客户端添加商品到购物车序列化类
    """
    class Meta:
        model = models.goodcart
        fields = ['productgood','productgood_num','user']

    def validate(self, attrs):
        """
        1、对数据进行校验
        2、写入数据库
        """
        productgood = attrs.get('productgood')
        productgood_num = attrs.get('productgood_num')
        user = attrs.get('user')
        if not (productgood and productgood_num and user):
            raise ValidationError({'detail':'关键参数缺失'})
        return attrs

    def create(self, validated_data):
        goodcart_obj = models.goodcart.objects.create(**validated_data)
        logger.warning('用户:%s,已将商品(id):%s,添加至购物车,添加数量为%s'%(validated_data.get('user'),
                                                                        validated_data.get('productgood'),
                                                                        validated_data.get('productgood_num')))
        return goodcart_obj



from lib.iPay import alipay,gateway
from django.conf import settings
from django.db import transaction
class PayModelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.order
        fields = ['order_title','pay_price']

    def validate(self, attrs):
        """
        1、对比付款价格与商品价格是否相等（包含数量）
            并取出所有商品对象和对应的数量，以字典的方式返回出去
        2、获取付款用户
        3、生成唯一订单号（uuid）
        4、生成支付链接
        5、入库前准备
            将pay_url放入context中，将order_id,user,order_addr放入attrs中
        6、create方法写入库中
        """
        productgoods_dic = self._checkout_pay_price(attrs)
        user = self._get_pay_user()
        order_id_list = self._get_uuid()
        pay_url = self._get_pay_url(attrs,order_id_list)
        self._stand_by_create(attrs,user,order_id_list,pay_url)
        # attrs.pop('productgoods')
        attrs['productgoods_dic'] = productgoods_dic
        return attrs

    def _checkout_pay_price(self,attrs):
        """
        "pay_num":{"4541968687606792193":"1","4541970878803476481":"1"}
        判断价格是否相等
        并取出所有商品对象和对应的数量，以字典的方式返回出去
        """
        pay_price = float(attrs.get('pay_price'))
        pay_num = self.context.get('pay_num')
        real_price = 0
        productgoods_dic = {}
        for product in pay_num:
            productgoods_obj = models.productgoods.objects.filter(id=product).first()
            buy_number = int(pay_num[product])
            calculate_price = productgoods_obj.price*buy_number
            real_price +=calculate_price
            productgoods_dic.setdefault(productgoods_obj,buy_number)

        if pay_price != real_price:
            raise ValidationError({'detail':'价格不正确'})
        return productgoods_dic

    def _get_pay_user(self):
        """
        从headers中取到HTTP_OPENID从而得到user
        :return:
        """
        request =  self.context.get('request')
        open_id = request.META.get('HTTP_OPENID')
        user = models.user.objects.filter(user_openid=open_id).first()

        return user

    def _get_uuid(self):
        """
        不管够买一个还是多个，订单号只返回一次
        """
        import uuid
        pay_num = self.context.get('pay_num')
        uuid_list = []
        for i in pay_num:
            uid = str(uuid.uuid4())
            new_uuid = uid.replace('-','')
            uuid_list.append(new_uuid)
        return uuid_list

    def _get_pay_url(self,attrs,order_id_list):
        """
        生成支付链接
        """
        joint_url = alipay.api_alipay_trade_page_pay(
            subject=attrs.get('order_title'),
            total_amount=float(attrs.get('pay_price')),
            out_trade_no=order_id_list[0],
            return_url=settings.RETURN_URL,
            notify_url=settings.NOTIFY_URL

        )
        pay_url = gateway+joint_url

        return pay_url

    def _stand_by_create(self,attrs,user,order_id_list,pay_url):
        """
        将pay_url放入context中，将order_id,user,order_addr放入attrs中
        """
        attrs['order_id_list'] = order_id_list
        attrs['user'] = user
        order_addr = self.context.get('order_addr')
        order_addr_obj = models.address.objects.filter(user=order_addr,is_default=True).first()
        attrs['order_addr'] = order_addr_obj
        self.context['pay_url'] = pay_url

    def create(self, validated_data):
        """
        写入数据库时来判断其购买的是单个还是多个
        """
        productgoods_dic = validated_data.pop('productgoods_dic')
        order_id_list = validated_data.pop('order_id_list')
        validated_data.pop('pay_price')
        if len(productgoods_dic) > 1:
            lis = []
            index = 0
            try: # 捕获异常
                for productgoods in productgoods_dic:
                    # 开启事务
                    with transaction.atomic():
                        order_obj = models.order.objects.create(**validated_data,
                                                                order_id = order_id_list[index],
                                                                productgoods = productgoods,
                                                                pay_price = productgoods.price,
                                                                buy_number = productgoods_dic[productgoods]
                                                                )
                        index += 1
                        lis.append(order_obj)
                logger.warning('用户:%s,预购买了商品id与数量:%s,收货地址是%s'%(validated_data.get('user'),
                                                                productgoods_dic,
                                                                validated_data.get('order_addr')))
            except Exception as e:
                logger.error('多次购买写入数据库出现错误，错误原因是:%s'%e)
                raise ValidationError({'detail':e})
            return lis
        if len(productgoods_dic) == 1:
            productgoods = list(productgoods_dic.keys())
            print(productgoods)
            order_obj = models.order.objects.create(**validated_data,
                                                    order_id=order_id_list[0],
                                                    productgoods=productgoods[0],
                                                    pay_price=productgoods[0].price,
                                                    buy_number=productgoods_dic.get(productgoods[0])
                                                    )
            logger.warning('用户:%s,预购买了商品id与数量:%s,收货地址是:%s' % (validated_data.get('user'),
                                                              productgoods_dic,
                                                              validated_data.get('order_addr')))
            return order_obj


class OrderlistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.order
        fields = ['order_status','order_id','order_title','pay_price','order_status_name',
                  'buy_number','trade_no','order_createtime','order_finishtime',
                  'pay_type','order_paytime','user','order_addr','oredr_detail',
                  'get_productgoods']

