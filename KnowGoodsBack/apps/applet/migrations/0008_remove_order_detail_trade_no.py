# Generated by Django 2.2.2 on 2021-10-14 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applet', '0007_auto_20211014_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_detail',
            name='trade_no',
        ),
    ]
