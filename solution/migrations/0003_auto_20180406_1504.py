# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-06 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solution', '0002_comment_point'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='point',
            new_name='points',
        ),
    ]
