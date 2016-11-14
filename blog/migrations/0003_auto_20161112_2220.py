# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_saleproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleproduct',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
