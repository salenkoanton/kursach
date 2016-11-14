# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0001_initial'),
        ('user', '0002_author_image'),
        ('blog', '0003_auto_20161112_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.TextField()),
                ('audio', models.ManyToManyField(related_name='post', to='audio.Audio')),
            ],
        ),
        migrations.DeleteModel(
            name='SaleProduct',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(to='user.User'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(related_name='post', to='user.Image'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='liked', to='user.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(to='user.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='blog.Post'),
        ),
    ]
