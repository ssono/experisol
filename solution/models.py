# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
"""
comments
modules
sections
*users
*likes
"""
# Create your models here.

class Module(models.Model):
    title = models.CharField(max_length=50)

class Comment(models.Model):
    module = models.ForeignKey(Module, null=True, blank=True)
    par_comment = models.ForeignKey('self', null=True, blank=True)
    content = models.TextField()

class Section(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    module = models.ForeignKey(Module)
