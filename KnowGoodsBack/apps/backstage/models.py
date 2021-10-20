from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# 后台用户表基于django内置表扩充字段
class UserInfo(AbstractUser):
    phone_code = models.CharField(max_length=11,unique=True,verbose_name='后台用户电话号码')
    icon = models.ImageField(upload_to='backavatar',default='backavatar/default.png')
    class Meta:
        verbose_name = '后台端用户表'
        verbose_name_plural = verbose_name

