# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-17 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0005_auto_20180414_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='next_sect',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='right', to='solution.Section'),
        ),
        migrations.AddField(
            model_name='section',
            name='prev_sect',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left', to='solution.Section'),
        ),
    ]
