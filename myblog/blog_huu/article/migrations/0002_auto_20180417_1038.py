# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='articles',
            field=models.ManyToManyField(blank=True, null=True, to='article.Article'),
        ),
    ]
