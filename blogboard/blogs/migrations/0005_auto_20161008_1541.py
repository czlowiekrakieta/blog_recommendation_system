# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20161004_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='date',
            new_name='timestamp',
        ),
    ]