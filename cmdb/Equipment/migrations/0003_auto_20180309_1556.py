# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0002_equipment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='cpu_count',
        ),
        migrations.AddField(
            model_name='equipment',
            name='cpu',
            field=models.CharField(max_length=32, null=True, verbose_name=b'CPU\xe4\xbf\xa1\xe6\x81\xaf', blank=True),
        ),
    ]
