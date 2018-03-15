# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0003_auto_20180309_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=32, verbose_name=b'\xe5\x80\xbc')),
                ('types', models.CharField(max_length=32, verbose_name=b'token\xe7\xb1\xbb\xe5\x9e\x8b')),
                ('time', models.DateTimeField(verbose_name=b'\xe6\xb3\xa8\xe5\x86\x8c\xe6\x97\xb6\xe9\x97\xb4')),
            ],
        ),
    ]
