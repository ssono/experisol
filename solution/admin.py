# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from solution.models import Module, Comment, Section, TotalStats, UserStats, Project
from django.contrib import admin

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order',  'pk')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'module')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'points','module', 'par_comment', 'content')

class TotalStatsAdmin(admin.ModelAdmin):
    list_display = ('uniqueUsers', 'totalComments', 'totalVotes', 'totalTime', 'avgTime')

class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('ipHash', 'timeSpent', 'comments', 'votes')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'pk')
# Register your models here.
admin.site.register(Module, ModuleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(TotalStats, TotalStatsAdmin)
admin.site.register(UserStats, UserStatsAdmin)
admin.site.register(Project, ProjectAdmin)
