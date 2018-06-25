from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div ,Row
from app.models import Sample
import string
import random

def generate_uniq_id(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))





class SamplesForm(forms.Form):

    samples = Sample.objects.all()



    fluids =[(None, "All")] + [(element,element) for element in list(set(samples.values_list('Fluid', flat=True)))]
    health_choice =[(None, "All")] + [(element,element) for element in list(set(samples.values_list('Healthy', flat=True)))]
    extraction_choice =[(None, "All")] + [(element,element) for element in list(set(samples.values_list('Extraction', flat=True)))]
    #extraction_choice =
    sex_choice = (("All", ""), ("All (only annotated)", "mf"),("Male","male"),("Female","female"))
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
                    Submit('submit', 'SEARCH', css_class='btn btn-primary')
                    # onsubmit="alert('Neat!'); return false")
                ),
                css_class='form-row')
        )

        def generate_id(self):
            is_new = True
            while is_new:
                pipeline_id = generate_uniq_id()
                if not os.path.exists():
                    return pipeline_id
