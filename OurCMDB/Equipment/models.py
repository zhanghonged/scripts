#coding:utf-8
from django.db import models

# Create your models here.
class Equipment(models.Model):
    hostname = models.CharField(max_length = 32, verbose_name='服务器名称')
    system = models.CharField(max_length = 32, verbose_name='服务器系统')
    mac = models.CharField(max_length = 32, verbose_name='MAC地址')
    ip = models.CharField(max_length = 32, verbose_name='IP地址')
    statue = models.CharField(max_length=32, verbose_name='服务器状态')
    user = models.CharField(max_length = 32, verbose_name='用户名')
    password = models.CharField(max_length = 32, verbose_name='密码')
