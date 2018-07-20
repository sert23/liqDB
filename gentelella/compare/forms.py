from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div ,Row, HTML
from app.models import Sample
import string
import random
import os
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT
from django.db.models import Q


def generate_uniq_id(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


samples = Sample.objects.all()
fluid_list = list(set(samples.values_list('Fluid', flat=True)))
health_list = list(set(samples.values_list('Healthy', flat=True)))
extraction_list = list(set(samples.values_list('Extraction', flat=True)))
sex_list = list(set(samples.values_list('Sex', flat=True)))
library_list = list(set(samples.values_list('Library', flat=True)))


class CompareForm(forms.Form):

    fluids =[(None, "All")] + [(element,element) for element in sorted(fluid_list,key=str.lower)]
    health_choice =[(None, "All")] + [(element,element) for element in health_list]
    extraction_choice =[(None, "All")] + [(element,element) for element in sorted(extraction_list,key=str.lower)]
    #extraction_choice =
    sex_choice = [(None, "Both")] +  [("mf", "Both (only annotated)")]+[(element,element) for element in sex_list]
    #sex_choice = (("", "All"), ("mf", "mf"),("male","male"),("female","female"))
    library_choice = [(None, "All")] + [(element,element) for element in  sorted(library_list,key=str.lower)]
    #extraction_choice = [""] + list(set(samples.values_list('Extraction', flat=True)))
    #library_choice = [""] + list(set(samples.values_list('Library', flat=True)))
    #fluids = samples.values_list('Fluid', flat=True)
    fluid =  forms.ChoiceField(label="Fluid",choices=fluids,required=False)
    sex =  forms.ChoiceField(label="Sex",choices=sex_choice,required=False)
    healthy =  forms.ChoiceField(label="Healthy Subjects",choices=health_choice,required=False)
    extraction =  forms.ChoiceField(label="RNA Extraction Protocol",choices=extraction_choice,required=False)
    library =  forms.ChoiceField(label="RNA Library Preparation",choices=library_choice,required=False)

    fluid2 = forms.ChoiceField(label="Fluid", choices=fluids, required=False)
    sex2 = forms.ChoiceField(label="Sex", choices=sex_choice, required=False)
    healthy2 = forms.ChoiceField(label="Healthy Subjects", choices=health_choice, required=False)
    extraction2 = forms.ChoiceField(label="RNA Extraction Protocol", choices=extraction_choice, required=False)
    library2 = forms.ChoiceField(label="RNA Library Preparation", choices=library_choice, required=False)

    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(CompareForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(HTML("""<h3> First Group</h3>""")),
            Div(
                #Fieldset(

                Field('fluid', wrapper_class='col-md-2',css_class='form-control'),
                Field('sex', wrapper_class='col-md-2',css_class='form-control'),
                Field('healthy', wrapper_class='col-md-2',css_class='form-control'),
                Field('extraction', wrapper_class='col-md-2',css_class='form-control'),
                Field('library', wrapper_class='col-md-2',css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'COMPARE', onclick="$('#loadpage').show(); $('#divPageContent').hide();", css_class='btn btn-primary btn-form')
                    # onsubmit="alert('Neat!'); return false")
                ),
                css_class='form-row'),
            Row(HTML("""<h3> Second Group</h3>""")),
            Div(
                # Fieldset(

                Field('fluid2', wrapper_class='col-md-2', css_class='form-control'),
                Field('sex2', wrapper_class='col-md-2', css_class='form-control'),
                Field('healthy2', wrapper_class='col-md-2', css_class='form-control'),
                Field('extraction2', wrapper_class='col-md-2', css_class='form-control'),
                Field('library2', wrapper_class='col-md-2', css_class='form-control'),
                # ButtonHolder(
                #     # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                #     Submit('submit', 'FILTER', onclick="$('#loadpage').show(); $('#divPageContent').hide();",
                #            css_class='btn btn-primary btn-form')
                #     # onsubmit="alert('Neat!'); return false")
                # ),
                css_class='form-row')
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
        fluid2 = str(cleaned_data.get("fluid2"))
        sex2 = str(cleaned_data.get("sex2"))
        healthy2 = str(cleaned_data.get("healthy2"))
        extraction2 = str(cleaned_data.get("extraction2"))
        library2 = str(cleaned_data.get("library2"))
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


        if fluid2:
            fluid_list2 = [fluid2]
        else:
            fluid_list2 = list(set(samples.values_list('Fluid', flat=True)))
        if sex2:
            if sex2 == "mf":
                sex_list2 = ["male","female"]
            else:
                sex_list2 = [sex2]
        else:
            sex_list2 = list(set(samples.values_list('Sex', flat=True)))
        if healthy2:
            health_list2 = [healthy2]
        else:
            health_list2 = list(set(samples.values_list('Healthy', flat=True)))

        if extraction2:
            extraction_list2=[extraction2]
        else:
            extraction_list2 = list(set(samples.values_list('Extraction', flat=True)))

        if library2:
            library_list2=[library2]
        else:
            library_list2 = list(set(samples.values_list('Library', flat=True)))

        querySamples = Sample.objects.all().filter(Fluid__in=fluid_list).filter(Sex__in=sex_list).filter(Healthy__in=health_list).filter(Extraction__in=extraction_list).filter(Library__in=library_list).values_list('Experiment', flat=True)
        querySamples2 = Sample.objects.all().filter(Fluid__in=fluid_list2).filter(Sex__in=sex_list2).filter(Healthy__in=health_list2).filter(Extraction__in=extraction_list2).filter(Library__in=library_list2).values_list('Experiment', flat=True)

        queryString = ",".join(querySamples).strip(' ')
        queryString2 = ",".join(querySamples2).strip(' ')

        sampleString = queryString + ","+ queryString2
        query_n = len(queryString.split(","))
        query_n2 = len(queryString2.split(","))
        groupList= ["Group1"]*query_n + ["Group2"]*query_n2

        sampleGroups = ",".join(groupList)

        query_path = os.path.join(DATA_FOLDER,"queryData", query_id)
        outputPath = os.path.join(query_path,"queryOutput")
        #sampleGroups=""

        call = "java -jar /opt/sRNAtoolboxDB/exec/liqDB.jar output={outputPath} mode=DE sampleString={sampleString} sampleGroups={sampleGroups}  variables=Groups".format(
            outputPath=outputPath,
            sampleString=sampleString,
            sampleGroups=sampleGroups,


        )
        with open(os.path.join(query_path,"query.txt"), "w") as text_file:
            text_file.write(sampleString)
        with open(os.path.join(query_path,"call.txt"), "w") as text_file:
            text_file.write(call)
            text_file.write("\n"+ str(len(groupList)) +"\n")
            text_file.write(str(groupList.count("Group1"))+" Group1 ")
            text_file.write(str(groupList.count("Group2"))+" Group2 ")
            text_file.write(str(sampleString.count(","))+" SampleString")
            text_file.write(str(queryString.count(","))+" queryString")
            text_file.write(str(queryString2.count(","))+" queryString2")


        #print(query_id,fluid,sex,healthy,extraction,library)
        return(query_id,call)
    def start_query(self):
        query_id = self.generate_id()
        return self.make_query(self.cleaned_data,query_id)

