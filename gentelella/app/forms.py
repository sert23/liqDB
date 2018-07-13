from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div ,Row
from app.models import Sample
import string
import random
import os
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT
from django.db.models import Q


def generate_uniq_id(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ContactForm(forms.Form):

    email_input=forms.EmailField(label="Please enter your email in case we should contact you (not required)", required=False)
    name_input=forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    info=forms.CharField(label="Sample/Project info",widget=forms.Textarea(attrs={'placeholder': 'Please include SRP/SRA ids and any extra info you deem useful for the DB'}))
    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

                Field('email_input',css_class='form-control'),
                Field('name_input',css_class='form-control'),
                Field('info', css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'FILTER', onclick="$('#loadpage').show(); $('#divPageContent').hide();", css_class='btn btn-primary btn-form')
                    # onsubmit="alert('Neat!'); return false")
                )

        )

    def generate_id(self):
        is_new = True
        while is_new:
            query_id = generate_uniq_id()
            #query_path =os.path.join(MEDIA_ROOT,query_id)
            query_path =os.path.join(DATA_FOLDER,"queryData",query_id)
            if not os.path.exists(query_path):
                os.mkdir(query_path)
                return query_id

    def make_query(self,cleaned_data,query_id):

        fluid = str(cleaned_data.get("fluid"))
        sex = str(cleaned_data.get("sex"))
        healthy = str(cleaned_data.get("healthy"))
        extraction = str(cleaned_data.get("extraction"))
        library = str(cleaned_data.get("library"))
        samples = Sample.objects.all()
        #samples = Sample.objects.all()

        #print(samples)

        if fluid:
            fluid_list = [fluid]
        else:
            fluid_list = list(set(samples.values_list('Fluid', flat=True)))
        if sex:
            if sex == "mf":
                sex_list = ["male","female"]
            else:
                sex_list = [sex]
        else:
            sex_list = list(set(samples.values_list('Sex', flat=True)))
        if healthy:
            health_list = [healthy]
        else:
            health_list = list(set(samples.values_list('Healthy', flat=True)))

        if extraction:
            extraction_list=[extraction]
        else:
            extraction_list = list(set(samples.values_list('Extraction', flat=True)))

        if library:
            library_list=[library]
        else:
            library_list = list(set(samples.values_list('Library', flat=True)))

        querySamples = Sample.objects.all().filter(Fluid__in=fluid_list).filter(Sex__in=sex_list).filter(Healthy__in=health_list).filter(Extraction__in=extraction_list).filter(Library__in=library_list).values_list('Experiment', flat=True)

        queryString = ",".join(querySamples)
        #print(len(querySamples))
        #samples_ids = samples.values_list('Experiment',flat=True)
        #print(samples_ids)
        #print(len(samples_ids))

        query_path = os.path.join(DATA_FOLDER,"queryData", query_id)
        outputPath = os.path.join(query_path,"queryOutput")

        call = "java -jar /opt/sRNAtoolboxDB/exec/liqDB.jar output={outputPath} mode=matrix sampleString={sampleString}".format(
            outputPath=outputPath,
            sampleString=queryString
        )


        with open(os.path.join(query_path,"query.txt"), "w") as text_file:
            text_file.write(queryString)
        #print(query_id,fluid,sex,healthy,extraction,library)
        return(query_id,call)
    def start_query(self):
        query_id = self.generate_id()
        return self.make_query(self.cleaned_data,query_id)
