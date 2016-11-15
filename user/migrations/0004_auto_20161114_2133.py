# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(to='user.Image', default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.BooleanField(default=True),
        ),
    ]
