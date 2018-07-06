# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from solution.models import Module, Comment, Section, TotalStats, SessionStats, Project, Profile, Email
from django.contrib import admin

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'project',  'pk')
    list_filter = ('project',)

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'module')
    list_filter = ('module',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'points','module', 'par_comment', 'content', 'pk')
    list_filter = ('module', 'par_comment',)

class TotalStatsAdmin(admin.ModelAdmin):
    list_display = ('uniqueUsers', 'totalComments', 'totalVotes', 'totalTime', 'avgTime')

class SessionStatsAdmin(admin.ModelAdmin):
    list_display = ('ipHash', 'timeSpent', 'comments', 'votes')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'created', 'points', 'pk')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined', 'points', 'email')

class EmailAdmin(admin.ModelAdmin):
    list_display = ('email',)

# Register your models here.
admin.site.register(Module, ModuleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(TotalStats, TotalStatsAdmin)
admin.site.register(SessionStats, SessionStatsAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Email, EmailAdmin)
