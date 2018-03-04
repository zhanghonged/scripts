#coding:utf-8
from django.db import models

# Create your models here.
class Equipment(models.Model):
    hostname = models.CharField(max_length = 32, verbose_name='服务器名称',blank=True,null=True)
    system = models.CharField(max_length = 32, verbose_name='服务器系统',blank=True,null=True)
    mac = models.CharField(max_length = 32, verbose_name='MAC地址',blank=True,null=True)
    status = models.CharField(max_length=32, verbose_name='服务器状态',blank=True,null=True)
    ip = models.CharField(max_length = 32, verbose_name='IP地址')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length = 32, verbose_name='用户名')
    password = models.CharField(max_length = 32, verbose_name='密码')
