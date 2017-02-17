# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-14 23:43
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0025_auto_20170201_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=0, editable=False, populate_from='username'),
            preserve_default=False,
        ),
    ]