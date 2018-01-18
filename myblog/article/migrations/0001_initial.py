# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe6\xa0\x87\xe9\xa2\x98')),
                ('time', models.DateField(auto_now=True, verbose_name=b'\xe5\x8f\x91\xe8\xa1\xa8\xe6\x97\xa5\xe6\x9c\x9f')),
                ('img', models.ImageField(upload_to=b'images', verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x9b\xbe\xe7\x89\x87', blank=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'\xe6\x96\x87\xe5\xad\x97\xe5\x86\x85\xe5\xae\xb9', blank=True)),
                ('description', models.TextField(verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe5\xa7\x93\xe5\x90\x8d')),
                ('Email', models.EmailField(max_length=254, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe9\x82\xae\xe7\xae\xb1')),
                ('age', models.IntegerField(null=True, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe5\xb9\xb4\xe9\xbe\x84', blank=True)),
                ('gender', models.CharField(max_length=32, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', blank=True)),
                ('phone', models.CharField(max_length=32, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba', blank=True)),
                ('address', models.CharField(max_length=128, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80', blank=True)),
                ('photo', models.ImageField(upload_to=b'images', verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe5\xa4\xb4\xe5\x83\x8f', blank=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(to='article.Author'),
        ),
    ]
