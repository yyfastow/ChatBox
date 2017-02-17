# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 20:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_chat_time_posted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='chat',
            new_name='text',
        ),
        migrations.AddField(
            model_name='chat',
            name='comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Chat'),
        ),
        migrations.AddField(
            model_name='chat',
            name='distance_from_sourse',
            field=models.PositiveIntegerField(default=1),
        ),
    ]