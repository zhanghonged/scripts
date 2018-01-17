#coding:utf-8
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
# class Article(models.Model):
#     title = models.CharField(max_length=64,verbose_name='标题')
#     author = models.CharField(max_length=32,verbose_name='作者')
#     time = models.DateTimeField(auto_now=True,verbose_name='发表时间')
#     content = models.TextField('文章内容')
#
#     def __unicode__(self):
#         return self.title

class Article(models.Model):
    title = models.CharField(max_length=64,verbose_name='文章标题')
    time = models.DateField(auto_now=True,verbose_name='发表日期')
    author = models.ForeignKey('Author') #一个作者有多篇文章
    img = models.ImageField(upload_to='images',verbose_name='文章图片',blank=True)
    content = models.TextField('文章内容',blank=True)
    description = RichTextUploadingField(verbose_name='文章描述', blank=True)

    def __unicode__(self):
        return self.title

class Author(models.Model):
    #必填字段
    name = models.CharField(max_length=32,verbose_name='作者姓名')
    Email = models.EmailField(verbose_name='作者邮箱')
    #选填字段
    age = models.IntegerField(verbose_name='作者年龄',blank=True,null=True)
    gender = models.CharField(max_length=32,verbose_name='性别',blank=True)
    phone = models.CharField(max_length=32,verbose_name='手机',blank=True)
    address = models.CharField(max_length=128,verbose_name='地址',blank=True)
    #特殊字段
    photo = models.ImageField(upload_to='images',verbose_name='作者头像',blank=True)
    description = RichTextUploadingField(verbose_name='作者描述',blank=True)

    def __unicode__(self):
        return self.name


