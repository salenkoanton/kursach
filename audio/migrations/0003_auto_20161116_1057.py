# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0002_auto_20161114_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='file',
            field=models.FileField(upload_to='audio/', default=None),
        ),
    ]
