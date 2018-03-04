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
                ('hostname', models.CharField(max_length=32, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d')),
                ('mac', models.CharField(max_length=32, verbose_name=b'MAC\xe5\x9c\xb0\xe5\x9d\x80')),
                ('ip', models.CharField(max_length=32, verbose_name=b'ip\xe5\x9c\xb0\xe5\x9d\x80')),
                ('sys_type', models.CharField(max_length=32, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('sys_version', models.CharField(max_length=32, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac')),
                ('cpu_count', models.IntegerField(verbose_name=b'CPU\xe4\xb8\xaa\xe6\x95\xb0')),
                ('disk', models.CharField(max_length=32, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98')),
                ('memory', models.CharField(max_length=32, verbose_name=b'\xe5\x86\x85\xe5\xad\x98')),
            ],
        ),
    ]
