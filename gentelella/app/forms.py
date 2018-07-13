from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div ,Row
from app.models import Sample
import string
import random
import os
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT
from django.db.models import Q
from django.core.mail import send_mail


def generate_uniq_id(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ContactForm(forms.Form):

    email_input=forms.EmailField(label="Please enter your email in case we should contact you (not required)", required=False)
    name_input=forms.CharField(label="Please enter your name (not required)",widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    info=forms.CharField(label="Sample/Project info",widget=forms.Textarea(attrs={'placeholder': 'Please include SRP/SRA ids and any extra info you deem useful for the DB'}))
    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Is there some study/samples you would like to see included?",
                Field('email_input',css_class='form-control'),
                Field('name_input',css_class='form-control'),
                Field('info', css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'SEND', css_class='btn btn-primary btn-form')
                    # onsubmit="alert('Neat!'); return false")
                ))

        )

    def send_email(self):
        cleaned_data = self.cleaned_data
        send_mail('liqDB: New Data from '+ cleaned_data.get("name_input"), cleaned_data.get("info")+"\nCONTACT EMAIL: "+cleaned_data.get("email_input"), 'liquiddbase@gmail.com',
              ['eaparicioeaparicio@gmail.com'], fail_silently=False)

    def generate_id(self):
        is_new = True
        while is_new:
            query_id = generate_uniq_id()
            #query_path =os.path.join(MEDIA_ROOT,query_id)
            query_path =os.path.join(DATA_FOLDER,"queryData",query_id)
            if not os.path.exists(query_path):
                os.mkdir(query_path)
                return query_id

