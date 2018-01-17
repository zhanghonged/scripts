#coding:utf-8
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=64,verbose_name='标题')
    author = models.CharField(max_length=32,verbose_name='作者')
    time = models.DateTimeField(auto_now=True,verbose_name='发表时间')
    content = models.TextField('文章内容')

    def __unicode__(self):
        return self.title
