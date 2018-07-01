# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from solution.models import Module, Comment, Section, TotalStats, SessionStats, Project, Profile
from django.contrib import admin

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'project',  'pk')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'module')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'points','module', 'par_comment', 'content', 'pk')

class TotalStatsAdmin(admin.ModelAdmin):
    list_display = ('uniqueUsers', 'totalComments', 'totalVotes', 'totalTime', 'avgTime')

class SessionStatsAdmin(admin.ModelAdmin):
    list_display = ('ipHash', 'timeSpent', 'comments', 'votes')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'points', 'pk')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined', 'points', 'email')
# Register your models here.
admin.site.register(Module, ModuleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(TotalStats, TotalStatsAdmin)
admin.site.register(SessionStats, SessionStatsAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)
