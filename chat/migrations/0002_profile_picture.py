# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='nick.jpg', upload_to='images'),
        ),
    ]
