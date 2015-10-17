# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


def journal(request):
    students = (
        {'id': 1,
        'name': u'Деревенець Артем',},
        {'id': 2,
        'name': u'Осінній Ілля',},
        {'id': 3,
        'name': u'Панченко Роман',},
    )
    return render(request, 'students/attendance.html',{'students': students})