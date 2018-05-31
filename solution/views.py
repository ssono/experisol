# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse, JsonResponse
from solution.models import Section, Module, Comment, TotalStats, UserStats

#Stats views
def ensureTotalStats():
    numObjects = len(TotalStats.objects.all())
    if numObjects != 1:
        if numObjects > 1:
            TotalStats.objects.all().delete()
        newTS = TotalStats()
        newTS.save()


# Create your views here.
def intro(request):
    ensureTotalStats()
    return render(request, 'intro.html', {})


def post(request, mod_pk):
    ensureTotalStats()
    modules = Module.objects.all()
    current_module = Module.objects.get(pk=mod_pk)
    return render(request, 'solve.html', {'modules': modules, 'sections': current_module.section_set.all(), 'comments': current_module.comment_set.all(), 'current_module': current_module,})

def next_mod(request, mod_pk):
    modules = Module.objects.all()
    current_module = Module.objects.get(pk=mod_pk)
    if request.is_ajax():
        if current_module.next_mod != None:
            current_module = current_module.next_mod
        newdata = {'new_pk': str(current_module.pk)}
        return JsonResponse(newdata)
    return HttpResponse("<a href='/solution/'"+ mod_pk + "/><h1>Return</h1></a>")

def prev_mod(request, mod_pk):
    modules = Module.objects.all()
    current_module = Module.objects.get(pk=mod_pk)
    if request.is_ajax():
        try:
            current_module = current_module.prev_mod
        except Module.prev_mod.RelatedObjectDoesNotExist:
            pass
        newdata = {'new_pk': str(current_module.pk)}
        return JsonResponse(newdata)
    return HttpResponse("<a href='/solution/'"+ mod_pk + "/><h1>Return</h1></a>")



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

def create_comment(request):
    if request.method =='POST' and request.is_ajax():
        text = str(request.POST['text'])
        if text != "":
            new_mod_id = int(request.POST['parent_mod'])
            new_mod = Module.objects.get(pk=new_mod_id)
            new_com = Comment.objects.create(
                content=text,
                module=new_mod,
                points=0
            )
            new_com.save()
        return render(request, 'solve.html', {})
    return HttpResponse("Weird")

def create_reply(request):
    if request.method =='POST' and request.is_ajax():
        text = str(request.POST['text'])
        if text != "":
            par_com_id = int(request.POST['parent_com'])
            par_com = Comment.objects.get(pk=par_com_id)
            new_reply = Comment.objects.create(
                content=text,
                par_comment=par_com,
                points=0
            )
            new_reply.save()
        return render(request, 'solve.html', {})
    return HttpResponse("Weird")
