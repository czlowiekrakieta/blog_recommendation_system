# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20161007_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='downs',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='ups',
        ),
    ]