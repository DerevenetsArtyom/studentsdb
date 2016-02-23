# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.contrib import messages

# crispy_forms for front-end ( bootstrap)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # call original initializator
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    from_email = forms.EmailField(label=u'Ваша Емейл Адреса')
    subject = forms.CharField(label=u'Заголовок Листа', max_length = 128)
    message = forms.CharField(
        label=u'Текст повiдомлення',
        max_length=2560,
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 5}))


class ContactView(FormView):  # Use generic FormView
    template_name = 'contact_admin/form.html'  # Set template
    form_class = ContactForm  # Set form for showing

    # Check if form is valid
    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['from_email']
        try:  # Try to send a message if data is valid
            send_mail(subject, message, from_email, ['admin@gmail.com'])
        except Exception:
            messages.error(self.request, u'Сталась помилка при вiдправленнi.')
        else:
            messages.success(self.request, u'Повiдомлення успiшно вiдправлено')
        return super(ContactView, self).form_valid(form)

    def get_success_url(self):
        return reverse('contact_admin')


'''
# FUNCTION VIEW FOR CONTACT ADMIN
def contact_admin(request):
    # check if form was posted
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether user data is valid:
        if form.is_valid():
            # send email
            # form.cleaned_data already keeps data in appropriate view
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                message = u'Під час відправки листа виникла непередбачува напомилка.' \
                          u'Спробуйте скористатись даною формою пізніше.'
            else:
                message = u'Повідомлення успішно надіслане!'
                # redirect to same contact page with success message
            return HttpResponseRedirect(
                    u'%s?status_message=%s' % (reverse('contact_admin'), message))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    return render(request, 'contact_admin/form.html', {'form': form})
    '''
