# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20160824_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Post', max_length=25)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('chat', models.TextField(default='')),
                ('share', models.CharField(choices=[('Public', 'Public'), ('Friends', 'Friends')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Profile')),
            ],
        ),
    ]
