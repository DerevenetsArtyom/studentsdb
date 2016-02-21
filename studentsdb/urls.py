"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .settings import MEDIA_ROOT, DEBUG

from students.views.stud_view import StudentUpdateView, StudentDeleteView, StudentAddView

urlpatterns = patterns('',

    # Students urls
    url(r'^$', 'students.views.stud_view.students_list', name='home'),

    url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),

    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    url(r'^students/(?P<sid>\d+)/journal/$', 'students.views.stud_view.students_journal', name='students_journal'),

    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),

    # Groups urls
    url(r'^groups/$', 'students.views.groups_view.groups_list', name='groups'),

    url(r'^groups/add/$', 'students.views.groups_view.groups_add',    name='groups_add'),

    url(r'^groups/(?P<gid>\d+)/edit/$',    'students.views.groups_view.groups_edit',        name='groups_edit'),

    url(r'^groups/(?P<gid>\d+)/delete/$',    'students.views.groups_view.groups_delete',    name='groups_delete'),

    # Journal urls
    url(r'^journal/$', 'students.views.journal_view.journal', name='journal'),

    # Contact Admin Form
    url(r'^contact-admin/$', 'students.views.contact_admin.contact_admin',
        name='contact_admin'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
    )


if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))
