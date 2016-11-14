# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0002_auto_20161114_0859'),
        ('user', '0002_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='audio',
            field=models.ManyToManyField(related_name='users', to='audio.Audio'),
        ),
    ]
