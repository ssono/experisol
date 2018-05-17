# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-17 20:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0008_remove_module_prev_sect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='next_sect',
        ),
        migrations.AddField(
            model_name='module',
            name='next_mod',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev_mod', to='solution.Module'),
        ),
    ]
