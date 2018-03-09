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
                ('ip', models.CharField(max_length=32, verbose_name=b'ip\xe5\x9c\xb0\xe5\x9d\x80')),
                ('port', models.CharField(max_length=16, verbose_name=b'\xe7\xab\xaf\xe5\x8f\xa3')),
                ('username', models.CharField(max_length=32, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d')),
                ('password', models.CharField(max_length=32, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81')),
                ('sys_type', models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('sys_version', models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac', blank=True)),
                ('cpu_count', models.IntegerField(null=True, verbose_name=b'CPU\xe4\xb8\xaa\xe6\x95\xb0', blank=True)),
                ('disk', models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98', blank=True)),
                ('memory', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98', blank=True)),
                ('hostname', models.CharField(max_length=32, null=True, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d', blank=True)),
                ('mac', models.CharField(max_length=32, null=True, verbose_name=b'MAC\xe5\x9c\xb0\xe5\x9d\x80', blank=True)),
            ],
        ),
    ]
