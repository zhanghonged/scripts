# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'\xe6\x9d\x83\xe9\x99\x90\xe5\x90\x8d\xe7\xa7\xb0')),
                ('description', models.TextField(verbose_name=b'\xe6\x9d\x83\xe9\x99\x90\xe6\x8f\x8f\xe8\xbf\xb0')),
                ('obj_id', models.IntegerField(verbose_name=b'\xe6\x9d\x83\xe9\x99\x90\xe5\xaf\xb9\xe8\xb1\xa1')),
            ],
        ),
        migrations.CreateModel(
            name='Permission_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission_id', models.IntegerField(verbose_name=b'\xe6\x9d\x83\xe9\x99\x90id')),
                ('user_id', models.IntegerField(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7id')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=32, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('password', models.CharField(max_length=32, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81')),
                ('phone', models.CharField(max_length=32, verbose_name=b'\xe6\x89\x8b\xe6\x9c\xba\xe5\x8f\xb7')),
                ('photo', models.ImageField(upload_to=b'image', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\xa4\xb4\xe5\x83\x8f')),
                ('email', models.EmailField(max_length=254, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe9\x82\xae\xe7\xae\xb1')),
            ],
        ),
    ]
