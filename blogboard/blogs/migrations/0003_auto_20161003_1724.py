# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 17:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20161003_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfollowings',
            name='followers',
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='following',
            field=models.ManyToManyField(related_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
