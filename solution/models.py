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
    par_comment = models.ForeignKey('self', null=True, blank=True, related_name="comkids")
    points = models.IntegerField(default=0)
    content = models.TextField()

    class Meta:
        ordering = ['-points']

    def __str__(self):
        return str(self.pk)

class Section(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    next_sect = models.OneToOneField('self', null=True, blank=True, related_name="right")
    prev_sect = models.OneToOneField('self', null=True, blank=True, related_name="left")

    def __str__(self):
        return self.title
