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





class SamplesForm(forms.Form):

    samples = Sample.objects.all()
    fluids =[(None, "All")] + [(element,element) for element in list(set(samples.values_list('Fluid', flat=True)))]
    health_choice =[(None, "All")] + [(element,element) for element in list(set(samples.values_list('Healthy', flat=True)))]
    extraction_choice =[(None, "All")] + [(element,element) for element in list(set(samples.values_list('Extraction', flat=True)))]
    #extraction_choice =
    sex_choice = (("", "All"), ("mf", "mf"),("male","male"),("female","female"))
    library_choice = [(None, "All")] + [(element,element) for element in list(set(samples.values_list('Extraction', flat=True)))]
    #extraction_choice = [""] + list(set(samples.values_list('Extraction', flat=True)))
    #library_choice = [""] + list(set(samples.values_list('Library', flat=True)))
    #fluids = samples.values_list('Fluid', flat=True)
    fluid =  forms.ChoiceField(label="Fluid",choices=fluids,required=False)
    sex =  forms.ChoiceField(label="Sex",choices=sex_choice,required=False)
    healthy =  forms.ChoiceField(label="Healthy Subjects",choices=health_choice,required=False)
    extraction =  forms.ChoiceField(label="RNA Extraction Protocol",choices=extraction_choice,required=False)
    library =  forms.ChoiceField(label="RNA Library Preparation",choices=library_choice,required=False)

    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(SamplesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('fluid', wrapper_class='col-md-2',css_class='form-control'),
                Field('sex', wrapper_class='col-md-2',css_class='form-control'),
                Field('healthy', wrapper_class='col-md-2',css_class='form-control'),
                Field('extraction', wrapper_class='col-md-2',css_class='form-control'),
                Field('library', wrapper_class='col-md-2',css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'FILTER', css_class='btn btn-primary')
                    # onsubmit="alert('Neat!'); return false")
                ),
                css_class='form-row')
        )

    def generate_id(self):
        is_new = True
        while is_new:
            query_id = generate_uniq_id()
            query_path =os.path.join(MEDIA_ROOT,query_id)
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
        #print(samples)
        if fluid:
            samples = samples.filter(Fluid__exact=fluid)
            samples = samples.filter(Sex__exact="female")
        if sex:
            samples = samples.filter(Sex__exact="female")
            if sex == "mf":
                print("hello")
                to_exc = ["unavailable"]
                from django.db.models import Q


                #samples=samples

                #samples = samples.all().exclude(Sex__in=to_exc)
                #exclude()
            else:
                samples = samples.filter(Sex__exact=sex)
            print(sex)
            samples = samples.filter(Sex__exact=sex)
        if healthy:
            samples = samples.filter(Healthy__exact=healthy)
        if extraction:
            samples = samples.filter(Extraction__exact=extraction)
        if library:
            samples = samples.filter(Library__exact=library)

        samples_ids = samples.values_list('Experiment',flat=True)
        print(samples_ids)
        print(len(samples_ids))
        query_path = os.path.join(MEDIA_ROOT, query_id)
        print(query_id,fluid,sex,healthy,extraction,library)
        return(query_id)
    def start_query(self):
        query_id = self.generate_id()
        return self.make_query(self.cleaned_data,query_id)

