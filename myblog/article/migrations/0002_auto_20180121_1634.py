# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(default=b'images/default.jpg', upload_to=b'images', verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x9b\xbe\xe7\x89\x87', blank=True),
        ),
    ]
