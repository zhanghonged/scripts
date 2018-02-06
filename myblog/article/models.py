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
    img = models.ImageField(upload_to='images',default='images/default.jpg',verbose_name='文章图片',blank=True)
    content = RichTextUploadingField(verbose_name='文字内容',blank=True)
    description = models.TextField(verbose_name='文章描述', blank=True)
    category = models.CharField(max_length=50, verbose_name='文章分类', blank=True)
    tags = models.ManyToManyField('Tag',verbose_name='标签集合',blank=True)

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField('标签名',max_length=20)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    def __unicode__(self):
        return self.name

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


