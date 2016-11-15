# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20161115_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.NullBooleanField(choices=[(True, 'male'), (False, 'female')], default=True),
        ),
    ]
