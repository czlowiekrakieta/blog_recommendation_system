# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-17 13:53
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blogs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ManageCalculations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_eval', models.DateTimeField(default=datetime.datetime(2010, 1, 1, 0, 0, tzinfo=utc))),
                ('last_regression', models.DateTimeField(default=datetime.datetime(2010, 1, 1, 0, 0, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='MostPopularByCat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('last_eval', models.DateTimeField(default=datetime.datetime(2010, 1, 1, 0, 0, tzinfo=utc))),
                ('blogs', models.ManyToManyField(related_name='pop_blogs', to='blogs.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
                ('similar', models.ManyToManyField(related_name='similar', to='blogs.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similar', models.ManyToManyField(related_name='similar', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blogs.UserFollowings')),
            ],
        ),
    ]