# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse, JsonResponse
from solution.models import Section, Module, Comment, TotalStats, SessionStats, Project, Email
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, timezone
from ipware import get_client_ip
from django.core.mail import send_mail
from django.conf import settings


#Stats views

###############################################################################

def intro(request):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
    html = 'intro.html'
    if request.user_agent.is_mobile:
        html = 'mobintro.html'
    return render(request, html, {})


def post(request, proj_pk,  mod_pk):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
    proj = Project.objects.get(pk=proj_pk)
    modules = proj.modules.all()
    current_module = Module.objects.get(pk=mod_pk)
    authors = ", ".join([p.user.username for p in proj.authors.all()])
    html = 'solve.html'
    if request.user_agent.is_mobile:
        html = 'mobsolve.html'
    return render(request, html, {'modules': modules, 'sections': current_module.sections.all(), 'comments': current_module.comments.all(), 'current_module': current_module, 'project': proj, 'authors': authors})

def email(request):
    if request.method == 'GET':
        html = 'email.html'
        if request.user_agent.is_mobile:
            html = 'mobemail.html'
        print(html)
        return render(request, html, {})
    elif request.is_ajax() and request.method == 'POST':
        # new_email = request.POST['new_email']
        # subject = 'Thank You'
        # message = "Hello!\n\n Thanks for showing interest in Solvent. I'll let you know when we launch \n\n -ssono"
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [new_email,]
        # send_mail( subject, message, email_from, recipient_list )

        new_em_obj = Email.objects.create(email=new_email)
        html = 'email.html'
        if request.user_agent.is_mobile:
            html = 'mobemail.html'
        return render(request, html, {})
    else:
        return HttpResponse("How did you get here?")

#############################################################################


def next_mod(request, proj_pk, mod_pk):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
    current_module = Module.objects.get(pk=mod_pk)
    project = Project.objects.get(pk=proj_pk)
    if request.is_ajax():
        if current_module.next_mod != None:
            current_module = current_module.next_mod
            newdata = {'mod_pk': str(current_module.pk), 'proj_pk': str(project.pk)}
            return JsonResponse(newdata)
        elif project.next_proj != None:
            project = project.next_proj
            modules = project.modules.all()
            if len(modules) > 0:
                current_module = modules[0]
            newdata = {'mod_pk': str(current_module.pk), 'proj_pk': str(project.pk)}
            return JsonResponse(newdata)
        else:
            newdata = {'mod_pk': '-1', 'proj_pk': '-1'}
            return JsonResponse(newdata)


    return HttpResponse("<a href='/"+ str(proj_pk) + "/" + str(mod_pk) + "'/><h1>Return</h1></a>")

def prev_mod(request, proj_pk, mod_pk):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
    current_module = Module.objects.get(pk=mod_pk)
    if request.is_ajax():
        project = Project.objects.get(pk=proj_pk)
        try:
            current_module = current_module.prev_mod
        except Module.prev_mod.RelatedObjectDoesNotExist:
            try:
                project = project.prev_proj
                modules = project.modules.all()
                if len(modules) > 0:
                    current_module = modules[len(modules) - 1]
                else:
                    project = Project.objects.get(pk=proj_pk)
            except Project.prev_proj.RelatedObjectDoesNotExist:
                pass

        newdata = {'mod_pk': str(current_module.pk), 'proj_pk': str(project.pk)}
        return JsonResponse(newdata)
    return HttpResponse("<a href='/"+ str(proj_pk) + "/" + str(mod_pk) + "'/><h1>Return</h1></a>")



def comment_vote(request):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
        addVote(request)
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

def project_vote(request):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
        addVote(request)
    if request.method == 'POST' and request.is_ajax():
        proj_id = request.POST['proj_id']
        voting = Project.objects.get(pk=proj_id)
        voting.points += 1

        voting.save()
        newdata = {}
        newdata["points"] = voting.points
        return JsonResponse(newdata)
    return HttpResponse("Please return to the main site or I will be forced to warn you a second time!")

def create_comment(request):
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
        addComment(request)
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
    if not request.user.is_staff:
        ensureTotalStats()
        ipCheck(request)
        addComment(request)
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

##############################################################################

def addVote(request):
    ip = get_client_ip(request)
    if ip != None:
        ipHash = hash(ip)
        user = SessionStats.objects.get(ipHash=ipHash)
        user.votes += 1
        user.save()
    tstats = TotalStats.objects.all()[0]
    tstats.totalVotes += 1
    tstats.save()

def addComment(request):
    ip = get_client_ip(request)
    if ip != None:
        ipHash = hash(ip)
        user = SessionStats.objects.get(ipHash=ipHash)
        user.comments += 1
        user.save()
    tstats = TotalStats.objects.all()[0]
    tstats.totalComments += 1
    tstats.save()

def newUser(ipHash):
    tstats = TotalStats.objects.all()[0]
    user = SessionStats(ipHash=ipHash, lastAction=datetime.now(timezone.utc), totalstats=tstats)
    user.save()
    tstats.uniqueUsers += 1
    tstats.save()
    return

def ensureTotalStats():
    numObjects = len(TotalStats.objects.all())
    if numObjects != 1:
        if numObjects > 1:
            TotalStats.objects.all().delete()
        newTS = TotalStats()
        newTS.save()

def ipCheck(request):
    ip = get_client_ip(request)
    if ip != None:
        ipHash = hash(ip)
        logUserInteraction(ipHash)

def logUserInteraction(ipHash):
    tstats = TotalStats.objects.all()[0]
    try:
        user = SessionStats.objects.get(ipHash=ipHash)
    except ObjectDoesNotExist:
        newUser(ipHash)
        return
    #update lastaction and timespent of less than 30 min between actions
    #update totaltime and avg user time
    now = datetime.now(timezone.utc)
    tdiff = now - user.lastAction
    if tdiff.total_seconds() < 1800:
        user.timeSpent += tdiff
        tstats.totalTime += tdiff
        tstats.save()
        tstats.avgTime = newAvgTime()
    user.lastAction = now
    user.save()


def newAvgTime():
    tstats = TotalStats.objects.all()[0]
    timeInSec = int(tstats.totalTime.total_seconds())
    if tstats.uniqueUsers > 1:
        avgTime = timeInSec // tstats.uniqueUsers
        avgTime = timedelta(seconds=avgTime)
        tstats.avgTime = avgTime
    else:
        tstats.avgTime = tstats.totalTime
    tstats.save()
