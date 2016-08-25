# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 20:00
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='Phone Number', regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=150)),
                ('birthday', models.DateTimeField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
            ],
        ),
    ]
