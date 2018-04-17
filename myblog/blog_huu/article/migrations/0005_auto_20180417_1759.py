# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 09:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20180417_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=128)),
                ('post_time', models.DateTimeField(default=datetime.datetime(2018, 4, 17, 9, 59, 20, 510999, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='post_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 17, 9, 59, 20, 509038, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='articles', to='article.Tag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='article.Article'),
        ),
    ]
