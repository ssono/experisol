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

    def __str__(self):
        return self.title

class Comment(models.Model):
    module = models.ForeignKey(Module, null=True, blank=True)
    par_comment = models.ForeignKey('self', null=True, blank=True)
    points = models.IntegerField(default=0)
    content = models.TextField()

    def __str__(self):
        return self.module.title

class Section(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
