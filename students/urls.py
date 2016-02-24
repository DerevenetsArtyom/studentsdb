from django.conf.urls import patterns, include, url

from students.views.stud_view import StudentUpdateView, StudentDeleteView, StudentAddView
from students.views.contact_admin import ContactView


urlpatterns = patterns('',

    url(r'add/$', StudentAddView.as_view(), name='students_add'),

    url(r'(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),

    url(r'(?P<sid>\d+)/journal/$', 'students.views.stud_view.students_journal', name='students_journal'),

    url(r'(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
                       )