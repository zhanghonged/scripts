# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=32, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('system', models.CharField(max_length=32, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\xb3\xbb\xe7\xbb\x9f')),
                ('mac', models.CharField(max_length=32, verbose_name=b'MAC\xe5\x9c\xb0\xe5\x9d\x80')),
                ('ip', models.CharField(max_length=32, verbose_name=b'IP\xe5\x9c\xb0\xe5\x9d\x80')),
                ('statue', models.CharField(max_length=32, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe7\x8a\xb6\xe6\x80\x81')),
                ('user', models.CharField(max_length=32, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('password', models.CharField(max_length=32, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81')),
            ],
        ),
    ]
