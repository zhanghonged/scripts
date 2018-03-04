#coding:utf-8
from django.db import models

class Equipment(models.Model):
    hostname = models.CharField(max_length = 32, verbose_name='主机名')
    mac = models.CharField(max_length=32, verbose_name='MAC地址')
    ip = models.CharField(max_length=32, verbose_name='ip地址')
    sys_type = models.CharField(max_length=32, verbose_name='系统类型')
    sys_version = models.CharField(max_length=32, verbose_name='系统版本')
    cpu_count = models.IntegerField(verbose_name='CPU个数')
    disk = models.CharField(max_length=32, verbose_name='硬盘')
    memory = models.CharField(max_length=32, verbose_name='内存')

    def __unicode__(self):
        return self.hostname
# Create your models here.