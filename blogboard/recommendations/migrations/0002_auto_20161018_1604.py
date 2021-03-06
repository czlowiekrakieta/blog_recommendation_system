# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 16:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blog_coefficients'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='ManageCalculations',
        ),
    ]
