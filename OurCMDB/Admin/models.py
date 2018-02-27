#coding:utf-8
from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 32, verbose_name = '用户名')
    password = models.CharField(max_length = 32, verbose_name = '密码')
    phone = models.CharField(max_length=32, verbose_name = '手机号')
    photo = models.ImageField(upload_to='image', verbose_name = '用户头像')
    email = models.EmailField(verbose_name = '用户邮箱')

class Permission(models.Model):
    name = models.CharField(max_length = 32, verbose_name = '权限名称')
    description = models.TextField(verbose_name = '权限描述')
    obj_id = models.IntegerField(verbose_name="权限对象")

class Permission_user(models.Model):
    permission_id = models.IntegerField(verbose_name = '权限id')
    user_id = models.IntegerField(verbose_name = '用户id')