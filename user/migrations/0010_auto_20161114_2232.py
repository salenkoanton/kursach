# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20161114_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(null=True, blank=True, to='user.Image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='audio',
            field=models.ManyToManyField(related_name='users', null=True, to='audio.Audio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='following', null=True, to='user.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
