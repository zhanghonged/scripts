#coding:utf-8
from django.db import models

class Equipment(models.Model):

    ip = models.CharField(max_length=32, verbose_name='ip地址')
    port = models.CharField(max_length=16, verbose_name='端口')
    username = models.CharField(max_length = 32, verbose_name='用户名')
    password = models.CharField(max_length = 32, verbose_name='密码')
    status = models.CharField(max_length=32, verbose_name='连接状态', blank=True, null=True)
    sys_type = models.CharField(max_length=32, verbose_name='系统类型',blank=True,null=True)
    sys_version = models.CharField(max_length=32, verbose_name='系统版本',blank=True,null=True)
    cpu = models.CharField(max_length=32, verbose_name='CPU信息',blank=True,null=True)
    disk = models.CharField(max_length=32, verbose_name='硬盘',blank=True,null=True)
    memory = models.CharField(max_length=32, verbose_name='内存',blank=True,null=True)
    hostname = models.CharField(max_length = 32, verbose_name='主机名',blank=True,null=True)
    mac = models.CharField(max_length=32, verbose_name='MAC地址',blank=True,null=True)

    def __unicode__(self):
        return self.hostname
# Create your models here.