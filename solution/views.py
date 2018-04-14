# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse, JsonResponse
from solution.models import Section, Module, Comment
import json



# Create your views here.
def intro(request):
    return render(request, 'intro.html', {})


def post(request):
    modules = Module.objects.all()
    current_module = Module.objects.get(title="Table of Contents")
    return render(request, 'solve.html', {'modules': modules, 'sections': current_module.section_set.all(), 'comments': current_module.comment_set.all(),})


def comment_vote(request):
    if request.method == 'POST' and request.is_ajax():
        com_id = request.POST['com_id']
        weight = request.POST['weight']
        voting = Comment.objects.get(pk=com_id)
        voting.points += int(weight)
        voting.save()
        newdata = {}
        newdata["points"] = voting.points
        return JsonResponse(newdata)
    return HttpResponse("Please return to the main site or I will be forced to warn you a second time!")


"""
def comment_upvote(request):
    if request.method == 'POST' and request.is_ajax():
        com_id = request.POST['com_id']
        voting = Comment.objects.get(pk=com_id)
        voting.points += 1
        voting.save()
        newdata = {}
        newdata["points"] = voting.points
        return JsonResponse(newdata)
    return HttpResponse("Please return to the main site or I will be forced to warn you a second time!")
"""
