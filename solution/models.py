# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, time, datetime, date
"""
comments
modules
sections
*users
*likes
"""
# Create your models here.

#tite, next/prev_proj, modules, points, author
class Profile(models.Model):
    joined = models.DateField(default=date.today)
    points = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    #user.profile.stuff
    #Create Profile on creation of user
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

class Project(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Profile, blank=True, related_name="projects")
    next_proj = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="prev_proj")
    points = models.IntegerField(default=0)
    created = models.DateField(default=date.today, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_authors(self):
        return "\n".join([a.user.username for a in self.authors.all()])


class Module(models.Model):
    title = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="modules")
    next_mod = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="prev_mod")
    order = models.IntegerField(null=True, blank=True)
    class Meta:
            ordering = ['order']


    def __str__(self):
        return self.title

class Comment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    par_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="comkids")
    points = models.IntegerField(default=0)
    content = models.TextField()
    created = models.DateField(default=date.today, null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-points']

    def __str__(self):
        return str(self.pk)

class Section(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="sections")
    order = models.IntegerField(null=True, blank=True)

    class Meta:
            ordering = ['order']

    def __str__(self):
        return self.title

class TotalStats(models.Model):
    uniqueUsers = models.IntegerField(default=0)
    totalComments = models.IntegerField(default=0)
    totalVotes = models.IntegerField(default=0)
    totalTime = models.DurationField(default=timedelta())
    avgTime = models.DurationField(default=timedelta())

class SessionStats(models.Model):
    totalstats = models.ForeignKey(TotalStats, on_delete=models.CASCADE, null=True, blank=True)
    ipHash = models.BigIntegerField()
    timeSpent = models.DurationField(default=timedelta())
    comments = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    lastAction = models.DateTimeField()

class Email(models.Model):
    email = models.EmailField()
