# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
from django.contrib.auth.decorators import login_required



# Create your views here.
def intro(request):
    return render(request, 'intro.html', {})


def post(request):
    return HttpResponse("post")
