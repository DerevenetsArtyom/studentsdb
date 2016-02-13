# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from ..models.student import Student
from ..models.group import Group


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
    # Was form posted?
    # We use POST method for sending form to the server
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:  # field 'name' at button
            # Stack for errors
            errors = {}

            # Student's data validation

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}  # Initial data

            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
            # last name
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
            # birthday
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday
            # ticket
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
            # student_group
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]
            # photo
            photo = request.FILES.get('photo')
            if photo:
                if photo.size > 2*(10**6):  # File is greater than 2 MegaBytes
                    errors['photo'] = u"Розміp файлу більше 2 Мб"
                elif 'image' not in photo.content_type:  # File is not image
                    errors['photo'] = u"Файл не є зображенням"
                else:
                    data['photo'] = photo

            if not errors:  # dict is empty
                # create correct student object
                curr_st = u'%s %s' % (first_name, last_name)
                student = Student(**data)  # Unpacking data dict
                student.save()  # Save in DB
                # redirect user to students list
                # with correspond status message in URL and at page
                return HttpResponseRedirect(
                    u'%s?status_message=Студента %s успiшно додано!' % (reverse('home'), curr_st))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                       {'groups': Group.objects.all().order_by('title'),
                       'errors': errors})
        elif request.POST.get('cancel_button') is not None:  # User click to CANCEL
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                {'groups': Group.objects.all().order_by('title')})





def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)


def students_journal(request, sid):
    return HttpResponse('<h1> Student %s in journal</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
