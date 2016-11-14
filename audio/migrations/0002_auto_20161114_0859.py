# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='author',
            field=models.ForeignKey(related_name='audio', to='user.Author'),
        ),
    ]
