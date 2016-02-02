# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from ..models.student import Student


def students_list(request):
    # select all students from DB
    students = Student.objects.all()
    # try to order students list

    # Check if we get fey from GET dict
    order_by_key = request.GET.get('order_by', '')
    # Check if our key is among correspond keys for sorting
    # Else - just ignore it
    if order_by_key in ('last_name', 'first_name', 'ticket', 'id'):
        # Return QuerySet ordering by one of corresponding keys
        students = students.order_by(order_by_key)
        # in case if we click field again
        # it will be reverse
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # PAGINATE STUDENTS
    # Paginator class instance
    paginator = Paginator(students, 3)  # Show 3 contacts per page
    # get parameter 'page' from request
    page = request.GET.get('page')
    try:
        # method gets a number and
        # returns object Page ~ list of elements
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)


    return render(request, 'students/students_list.html',
        {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_journal(request,sid):
    return HttpResponse('<h1> Student %s in journal</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
