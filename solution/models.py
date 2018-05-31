# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
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
    next_mod = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="prev_mod")


    def __str__(self):
        return self.title

class Comment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    par_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="comkids")
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

    def __str__(self):
        return self.title

class TotalStats(models.Model):
    uniqueUsers = models.IntegerField(default=0)
    numComments = models.IntegerField(default=0)
    numVotes = models.IntegerField(default=0)
    totalTime = models.DurationField(default=datetime.timedelta())
    avgTime = models.DurationField(default=datetime.timedelta())

class UserStats(models.Model):
    totalStats = models.ForeignKey(TotalStats, on_delete=models.CASCADE, null=True, blank=True, related_name="userStatList")
    ipHash = models.IntegerField(default=0)
    timeSpent = models.DurationField(default=datetime.timedelta())
    comments = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
