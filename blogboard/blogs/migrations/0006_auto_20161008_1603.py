# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 16:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20161008_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollowings',
            name='followed_blogs',
            field=models.ManyToManyField(blank=True, null=True, to='blogs.Blog'),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]