# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-08 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_auto_20161008_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='culture',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='fashion',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='general_ratings',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='hard_science',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='politics',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='soft_science',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='sports',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='tech',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='travel',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='culture',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='fashion',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='hard_science',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='politics',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='soft_science',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='sports',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='tech',
            field=models.FloatField(default=2),
        ),
        migrations.AlterField(
            model_name='userfollowings',
            name='travel',
            field=models.FloatField(default=2),
        ),
    ]
