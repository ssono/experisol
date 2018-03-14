# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from solution.models import Module, Comment, Section
from django.contrib import admin

# Register your models here.
admin.site.register(Module)
admin.site.register(Comment)
admin.site.register(Section)
