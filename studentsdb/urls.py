from django.conf.urls import patterns, include, url
from django.contrib import admin

from .settings import MEDIA_ROOT, DEBUG

from students.views.contact_admin import ContactView

urlpatterns = patterns('',

    url(r'^$', 'students.views.stud_view.students_list', name='home'),

    # Students urls with namespace
    url(r'^students/', include('students.urls', namespace='students')),

    # Groups urls
    url(r'^groups/$', 'students.views.groups_view.groups_list', name='groups'),

    url(r'^groups/add/$', 'students.views.groups_view.groups_add',    name='groups_add'),

    url(r'^groups/(?P<gid>\d+)/edit/$',    'students.views.groups_view.groups_edit',        name='groups_edit'),

    url(r'^groups/(?P<gid>\d+)/delete/$',    'students.views.groups_view.groups_delete',    name='groups_delete'),

    # Journal urls
    url(r'^journal/$', 'students.views.journal_view.journal', name='journal'),

    # Contact Admin Form
    url(r'^contact-admin/$', ContactView.as_view(), name='contact_admin'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
    )

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT})
                            )
