# NOT ALREADY USE
# Add student manually
# validate form by hand and add it to DB if correct
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
                student = Student(**data)  # Unpacking data dict
                student.save()  # Save in DB
                # redirect user to students list
                # with correspond status message in URL and at page
                messages.success(request, u'Студента %s успiшно додано!' %  student)
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                       {'groups': Group.objects.all().order_by('title'),
                       'errors': errors})
        elif request.POST.get('cancel_button') is not None:  # User click to CANCEL
            # redirect to home page on cancel button
            messages.warning(request, u'Додавання студента вiдмiнено!')
            return HttpResponseRedirect(reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html',
                {'groups': Group.objects.all().order_by('title')})


# I tried to create form for student addition
# manually and process output data with StudentUpdateView(UpdateView)
class StudentUpdateFormByHand(forms.Form):
    # I spend a great deal of time making this method
    # works correct. But I did it!
    '''
    class StudentUpdateView(UpdateView):  # inherits from generic UpdateView
    form_class = StudentUpdateFormBYHand

    def get_initial(self):
        # Get saved data for student in dict_format
        stud_dict = Student.objects.values().get(id=self.object.id)
        # Set group name of it's id
        group_name_verbose = Group.objects.get(id=stud_dict['student_group_id'])
        # Add to initial dict name of group and get it in form
        stud_dict['student_group'] = group_name_verbose
        return stud_dict
        '''

    last_name = forms.CharField()
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    student_group = forms.ModelChoiceField(queryset=Group.objects.all())
    birthday = forms.DateField()
    ticket = forms.IntegerField()
    notes = forms.CharField(required=False)

    # Override save method. Works incorrect
    def save(self):
        data = self.cleaned_data
        st = Student(**data)
        st.save()

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('instance'):
            kwargs.pop('instance')
        super(StudentUpdateFormByHand, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students:students_edit',
           kwargs={'pk': self.initial['id']})
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
