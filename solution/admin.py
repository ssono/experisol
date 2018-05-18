# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from solution.models import Module, Comment, Section
from django.contrib import admin

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pk')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'points','module', 'par_comment', 'content')
# Register your models here.
admin.site.register(Module, ModuleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Section, SectionAdmin)
