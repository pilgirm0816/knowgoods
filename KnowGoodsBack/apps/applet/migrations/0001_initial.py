# Generated by Django 2.2.2 on 2021-10-14 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consignee', models.CharField(max_length=64, verbose_name='收件人姓名')),
                ('mobile', models.CharField(max_length=16, verbose_name='收件人联系方式')),
                ('address', models.CharField(max_length=256, verbose_name='收件人地址')),
                ('transportDay', models.CharField(default='', max_length=64, verbose_name='收货时间选择')),
                ('is_default', models.BooleanField(default=True, verbose_name='是否为默认地址')),
            ],
            options={
                'verbose_name': '用户地址表',
                'verbose_name_plural': '用户地址表',
            },
        ),
        migrations.CreateModel(
            name='good_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='商品分类名称')),
            ],
            options={
                'verbose_name': '商品分类表',
                'verbose_name_plural': '商品分类表',
            },
        ),
        migrations.CreateModel(
            name='good_categorychild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='商品分类具体名称')),
                ('img_url', models.CharField(max_length=256, null=True, verbose_name='图片地址')),
                ('category', models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='applet.good_category')),
            ],
            options={
                'verbose_name': '商品分类小表',
                'verbose_name_plural': '商品分类小表',
            },
        ),
        migrations.CreateModel(
            name='navar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navar_name', models.CharField(max_length=32, verbose_name='导航栏名称')),
                ('seq', models.IntegerField(verbose_name='导航栏的顺序排列')),
            ],
            options={
                'verbose_name': '首页导航表',
                'verbose_name_plural': '首页导航表',
            },
        ),
        migrations.CreateModel(
            name='productgoods',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True, verbose_name='商品编号')),
                ('name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='商品入库时间')),
                ('show_img', models.CharField(max_length=256, verbose_name='商品展示图片路径')),
                ('price', models.FloatField(verbose_name='商品优惠价格')),
                ('privilegePrice', models.FloatField(verbose_name='商品原价格')),
                ('discount', models.FloatField(default=7, verbose_name='折扣')),
                ('show_video', models.CharField(max_length=256, verbose_name='商品有关视频')),
                ('goods_type', models.IntegerField(choices=[(1, '电脑办公'), (2, '手机'), (3, '运动户外'), (4, '美妆护肤'), (5, '女装')], verbose_name='商品类型')),
                ('is_putaway', models.BooleanField(default=True, verbose_name='商品是否上架')),
                ('categorychild', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='applet.good_categorychild', verbose_name='商品所属分类')),
            ],
            options={
                'verbose_name': '商品表',
                'verbose_name_plural': '商品表',
            },
        ),
        migrations.CreateModel(
            name='productgoodsdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='商品标题')),
                ('stock_quantity', models.IntegerField(default=0, verbose_name='库存数量')),
                ('characteristic', models.CharField(max_length=128, verbose_name='商品规格')),
            ],
            options={
                'verbose_name': '商品详情信息表',
                'verbose_name_plural': '商品详情信息表',
            },
        ),
        migrations.CreateModel(
            name='productsale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='新品特卖名称')),
                ('img_url', models.CharField(max_length=128, verbose_name='图片地址')),
                ('type', models.CharField(default='temai', max_length=32, verbose_name='类型')),
                ('remark', models.CharField(max_length=64, verbose_name='新品特卖具体描述')),
            ],
            options={
                'verbose_name': '新品特卖表',
                'verbose_name_plural': '新品特卖表',
            },
        ),
        migrations.CreateModel(
            name='slideshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_name', models.CharField(max_length=128, verbose_name='轮播图名称')),
                ('img_url', models.TextField(verbose_name='轮播图图片路径')),
                ('is_show', models.BooleanField(default=True, verbose_name='图片是否展示')),
                ('click_url', models.CharField(max_length=256, verbose_name='图片的点击链接')),
            ],
            options={
                'verbose_name': '首页轮播图表',
                'verbose_name_plural': '首页轮播图表',
            },
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_openid', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='用户唯一标识')),
                ('username', models.CharField(max_length=128, verbose_name='微信用户的昵称')),
                ('sex', models.IntegerField(verbose_name='用户的性别，值为1时是男性，为2时是女性，0是未知')),
                ('country', models.CharField(max_length=64, verbose_name='用户所在国家')),
                ('province', models.CharField(max_length=64, verbose_name='用户所在省份')),
                ('city', models.CharField(max_length=64, verbose_name='用户所在城市')),
                ('language', models.CharField(max_length=32, verbose_name='用户所使用语言')),
                ('headingurl', models.TextField(verbose_name='用户头像地址')),
                ('user_level', models.IntegerField(choices=[(1, '普通会员'), (2, '白银会员'), (3, '黄金会员'), (4, '砖石会员')], verbose_name='用户的会员等级')),
                ('user_point', models.IntegerField(default=0, verbose_name='用户的积分')),
                ('user_balance', models.FloatField(default=0, verbose_name='用户余额')),
                ('user_createtime', models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')),
                ('user_isactive', models.BooleanField(default=True, verbose_name='用户是否激活')),
            ],
            options={
                'verbose_name': '小程序端用户表',
                'verbose_name_plural': '小程序端用户表',
            },
        ),
        migrations.CreateModel(
            name='productgoodsdetail_slideshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_slideshow', models.CharField(max_length=256, verbose_name='商品详情页轮播图')),
                ('productgoods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applet.productgoods', verbose_name='关联商品id')),
            ],
            options={
                'verbose_name': '商品详情页轮播图片表',
                'verbose_name_plural': '商品详情页轮播图片表',
            },
        ),
        migrations.CreateModel(
            name='productgoodsdetail_img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_img', models.CharField(max_length=256, verbose_name='商品详情页商品详情图片')),
                ('productgoods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applet.productgoods', verbose_name='关联商品id')),
            ],
            options={
                'verbose_name': '商品详情图片表',
                'verbose_name_plural': '商品详情图片表',
            },
        ),
        migrations.AddField(
            model_name='productgoods',
            name='detail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='applet.productgoodsdetail', verbose_name='商品详情信息'),
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=32, verbose_name='订单ID')),
                ('pay_price', models.FloatField(verbose_name='订单支付金额')),
                ('trade_no', models.CharField(max_length=64, null=True, verbose_name='流水号')),
                ('order_status', models.IntegerField(choices=[(1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '已签收'), (5, '待评价'), (6, '已评价')], verbose_name='订单状态')),
                ('freight', models.FloatField(default=0, verbose_name='订单运费')),
                ('logistics_company', models.CharField(max_length=64, verbose_name='物流公司')),
                ('logistics_number', models.CharField(max_length=128, verbose_name='物流订单编号')),
                ('order_createtime', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('order_finishtime', models.DateTimeField(null=True, verbose_name='订单完成时间')),
                ('order_paytime', models.DateTimeField(null=True, verbose_name='订单支付时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='订单在用户层面是否删除')),
                ('order_addr', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='applet.address', verbose_name='地址关联外键')),
                ('user', models.ForeignKey(on_delete=True, to='applet.user', verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '商品订单信息表',
                'verbose_name_plural': '商品订单信息表',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=True, to='applet.user', verbose_name='与哪个用户关联'),
        ),
    ]