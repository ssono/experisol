"""experisol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from solution import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.intro),
    path('<int:proj_pk>/next/<int:mod_pk>/', views.next_mod),
    path('<int:proj_pk>/prev/<int:mod_pk>/', views.prev_mod),
    path('<int:proj_pk>/<int:mod_pk>/', views.post),
    url(r'^com_vote/$', views.comment_vote),
    url(r'^proj_vote/$', views.project_vote),
    url(r'^create_comment/$', views.create_comment),
    url(r'^create_reply/$', views.create_reply),
    path('email/', views.email),
]
