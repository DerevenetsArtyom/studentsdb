# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import UpdateView, DeleteView, CreateView
from django.forms import ModelForm, Textarea
from django.contrib import messages
from django import forms

# Crispy forms for fronnt end (Bootstrap)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.student import Student


# List of student with ordering and pagination
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
    paginator = Paginator(students, 4)  # Show 4 contacts per page
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


# Add student using ModelForm
class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = ('last_name', 'first_name', 'middle_name', 'student_group',
                  'birthday', 'photo', 'ticket', 'notes')
        widgets = {
            'notes': Textarea(attrs={'rows': 5, 'cols': 5}),
        }
        template_name = 'students/students_add.html'

    # use crispy forms
    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes

        self.helper.form_action = reverse('students:students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = False
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
                ))


# CBV for adding student (use StudentAddForm)
class StudentAddView(CreateView):  # inherits from generic CreateView
    model = Student  # Required. Our model we are working with
    template_name = 'students/students_add.html'  # Path to the template for edit student
    form_class = StudentAddForm

    #  Returns the page after success operation
    def get_success_url(self):
        # Just message
        messages.success(self.request, u'Додавання студента успішне!')
        return reverse('home')

    # Custom the POST method
    # for redirection to home if it's a click to 'cancel'
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.error(self.request, u'Додавання студента вiдмiнено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentAddView, self).post(request, *args, **kwargs)


# Form for editing based on Student model (ModelForms)
class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = ('last_name', 'first_name', 'middle_name', 'student_group',
                  'birthday', 'photo', 'ticket', 'notes')
        widgets = {
            'notes': Textarea(attrs={'rows': 5, 'cols': 5}),
        }
        template_name = 'students/students_edit.html'

    # use crispy forms
    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes

        self.helper.form_action = reverse('students:students_edit',
            kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
                Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
                Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
                ))


class StudentUpdateView(UpdateView):  # inherits from generic UpdateView
    model = Student  # Required. Our model we are working with
    template_name = 'students/students_edit.html'  # Path to the template for edit student
    form_class = StudentUpdateForm

    #  Returns the page after success operation
    def get_success_url(self):
        # Just message
        messages.success(self.request, u'Редагування студента успішне!')
        return reverse('home')

    # Custom the POST method
    # for redirection to home if it's a click to 'cancel'
    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.error(self.request, u'Редагування студента вiдмiнено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        messages.info(self.request, u'Студента успiшно видалено!')
        return reverse('home')


def students_journal(request, sid):
    return HttpResponse('<h1> Student %s in journal</h1>' % sid)
