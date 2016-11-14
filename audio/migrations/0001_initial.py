# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_author_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='', default=None)),
                ('type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('rock', 'rock'), ('met_c', 'metalcore'), ('metal', 'metal'), ('hd_c', 'hardcore'), ('rap', 'rap')], max_length=5), size=40)),
                ('duration', models.TimeField(default=None)),
                ('author', models.ForeignKey(to='user.Author')),
            ],
        ),
    ]
