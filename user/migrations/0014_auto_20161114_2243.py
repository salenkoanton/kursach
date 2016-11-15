# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20161114_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, to='user.Image'),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.NullBooleanField(default=True),
        ),
    ]
