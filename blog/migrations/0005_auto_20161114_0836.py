# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20161114_0823'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('id',)},
        ),
    ]
