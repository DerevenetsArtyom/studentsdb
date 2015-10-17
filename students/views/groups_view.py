# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def groups_list(request):
    groups = (
        {'id': 1,
        'name': u'ДE-31',
        'leader': { 'id' : 1,'name' : u'Деревенець Артем',}},
        {'id': 2,
        'name': u'ДE-32',
        'leader': {"id" : 2,'name':u'Ильченко Анастасия',}},
        {'id': 3,
        'name': u'ДС-31',
        'leader': {'id':3,'name':u'Орлов Евгений',}},
        )
    return render(request, 'students/groups_list.html',{'groups':groups})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)

