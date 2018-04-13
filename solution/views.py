# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
from solution.models import Section, Module, Comment



# Create your views here.
def intro(request):
    return render(request, 'intro.html', {})


def post(request):
    modules = Module.objects.all()
    current_module = Module.objects.get(title="Table of Contents")
    return render(request, 'solve.html', {'modules': modules, 'sections': current_module.section_set.all(), 'comments': current_module.comment_set.all(),})

def comment_upvote(request):
    test= "test"
    if request.method == 'POST' and request.is_ajax():
        com_id = request.POST['com_id']
        voting = Comment.objects.get(pk=com_id)
        voting.points += 1
        voting.save()
        test = "wow"
    modules = Module.objects.all()
    current_module = Module.objects.get(title="Table of Contents")
    return render(request, 'solve.html', {'modules': modules, 'sections': current_module.section_set.all(), 'comments': current_module.comment_set.all(),})
