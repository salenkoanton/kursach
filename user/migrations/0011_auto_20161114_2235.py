# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20161114_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='information',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(upload_to='', default=None, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='audio',
            field=models.ManyToManyField(related_name='users', to='audio.Audio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following', to='user.User'),
        ),
    ]
