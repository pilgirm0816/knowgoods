# Generated by Django 2.2.2 on 2021-10-20 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applet', '0014_auto_20211020_1126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': '用户地址', 'verbose_name_plural': '用户地址'},
        ),
        migrations.AlterModelOptions(
            name='good_category',
            options={'verbose_name': '主分类', 'verbose_name_plural': '主分类'},
        ),
        migrations.AlterModelOptions(
            name='good_categorychild',
            options={'verbose_name': '子分类', 'verbose_name_plural': '子分类'},
        ),
        migrations.AlterModelOptions(
            name='goodcart',
            options={'verbose_name': '用户购物车', 'verbose_name_plural': '用户购物车'},
        ),
        migrations.AlterModelOptions(
            name='navar',
            options={'verbose_name': '首页导航栏', 'verbose_name_plural': '首页导航栏'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '订单列表', 'verbose_name_plural': '订单列表'},
        ),
        migrations.AlterModelOptions(
            name='productgoodsdetail',
            options={'verbose_name': '商品详情', 'verbose_name_plural': '商品详情'},
        ),
        migrations.AlterModelOptions(
            name='productgoodsdetail_img',
            options={'verbose_name': '详情页详情图片', 'verbose_name_plural': '详情页详情图片'},
        ),
        migrations.AlterModelOptions(
            name='productgoodsdetail_slideshow',
            options={'verbose_name': '详情页轮播图片', 'verbose_name_plural': '详情页轮播图片'},
        ),
        migrations.AlterModelOptions(
            name='productsale',
            options={'verbose_name': '新品特卖', 'verbose_name_plural': '新品特卖'},
        ),
        migrations.AlterModelOptions(
            name='slideshow',
            options={'verbose_name': '首页轮播图', 'verbose_name_plural': '首页轮播图'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '小程序端用户', 'verbose_name_plural': '小程序端用户'},
        ),
        migrations.AlterField(
            model_name='productgoodsdetail_img',
            name='productgoods',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='applet.productgoods', verbose_name='关联商品id'),
        ),
        migrations.AlterField(
            model_name='productgoodsdetail_slideshow',
            name='productgoods',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='applet.productgoods', verbose_name='关联商品id'),
        ),
    ]