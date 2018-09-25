from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div ,Row
from crispy_forms.bootstrap import FormActions
from app.models import Sample
import string
import random
import os
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT, BENCH_FOLDER
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy


def generate_uniq_id(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


samples = Sample.objects.all()

class BenchForm(forms.Form):
    benchID = forms.CharField(label="Input sRNAbench comma separated jobIDs", widget=forms.TextInput(attrs={'placeholder': 'e.g. SDS21JUI78,SD6D6DJDF9IK,S34R5TWT5GD7UJT48'}))
    queryGroup = forms.CharField(label="Group Name for selected samples from DB", widget=forms.TextInput(attrs={'placeholder': 'e.g. Healthy_DB'}))
    benchGroup = forms.CharField(label="Group Name for your sRNAbench jobs", widget=forms.TextInput(attrs={'placeholder': 'e.g. Cancer_uploaded'}))
    #field2=  forms.CharField(label=')', required=False)
    ##choices go here
    def __init__(self, *args, **kwargs):
        super(BenchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Div(
            #     Field('fluid', wrapper_class='col-md-2',css_class='form-control'),
            #     Field('sex', wrapper_class='col-md-2',css_class='form-control'),
            #     Field('healthy', wrapper_class='col-md-2',css_class='form-control'),
            #     Field('extraction', wrapper_class='col-md-2',css_class='form-control'),
            #     Field('library', wrapper_class='col-md-2',css_class='form-control'),
            #     css_class='form-row'),
            Div(
                Field('benchID', wrapper_class='col-md-3', css_class='form-control'),
                Field('queryGroup', wrapper_class='col-md-3', css_class='form-control'),
                Field('benchGroup', wrapper_class='col-md-3', css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'COMPARE', onclick="$('#loadpage').show(); $('#divPageContent').hide();", css_class='btn btn-primary btn-form')
                    # onsubmit="alert('Neat!'); return false")
                ),
                ButtonHolder(Submit('cancel', ' GO  BACK ', onclick="window.history.go(-1); return false;",
                                    css_class='btn btn-primary btn-form')),

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
        with open(os.path.join("/opt/liqDB/liqDB/gentelella/data_folder/queryData/XH2IPUFU5DKOJ8POR6KN","call.txt"), "w") as text_file:
            text_file.write(call)
        with open(os.path.join(query_path,"query.txt"), "w") as text_file:
            text_file.write(queryString)
        #print(query_id,fluid,sex,healthy,extraction,library)
        return(query_id,call)

    def make_DE(self,cleaned_data,query_id,old_query_id):
        with open(os.path.join(DATA_FOLDER,"queryData",old_query_id,"query.txt"), 'r') as queryfile:
            SRX_string = queryfile.read()
        sampleString = SRX_string
        query_n = len(SRX_string.split(","))
        DB_group = cleaned_data.get("queryGroup")
        sampleGroupList = [DB_group]* query_n
        sampleGroups = ",".join(sampleGroupList)
        userSampleString = cleaned_data.get("benchID")
        userSampleList = userSampleString.split(",")
        userSampleList = [x.strip(' ') for x in userSampleList ]
        userDirList = [os.path.join(BENCH_FOLDER,ID) for ID in userSampleList]
        userSampleString = ",".join(userDirList)
        userGroup = cleaned_data.get("benchGroup")
        user_n = len(userSampleString.split(","))
        userGroupList = [userGroup]* user_n
        userSampleGroups = ",".join(userGroupList)

        query_path = os.path.join(DATA_FOLDER, "queryData", query_id)
        outputPath = os.path.join(query_path, "queryOutput")

        call = "java -jar /opt/sRNAtoolboxDB/exec/liqDB.jar output={outputPath} mode=DE sampleString={sampleString} sampleGroups={sampleGroups} userSampleString={userSampleString} userSampleGroups={userSampleGroups} variables=Groups".format(

            outputPath=outputPath,
            sampleString=sampleString,
            sampleGroups=sampleGroups,
            userSampleString=userSampleString,
            userSampleGroups=userSampleGroups
        )

        with open(os.path.join(query_path, "call.txt"), "w") as text_file:
            text_file.write(call)

        with open(os.path.join(query_path,"query.txt"), "w") as text_file:
            text_file.write(sampleString)

        #os.system(call)

        #print(call)
        return query_id,call

    def start_DE(self, old_query_id):
        query_id = self.generate_id()
        return self.make_DE(self.cleaned_data,query_id, old_query_id)

class ManualForm(forms.Form):

    hiddenIDs = forms.CharField(label='', required=False, widget=forms.HiddenInput, max_length=1000000)

    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(ManualForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('hiddenIDs', name='hiddenIDs')),
                #Field('library', wrapper_class='col-md-2',css_class='form-control'),
                FormActions(
                # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    #Submit('submit', 'KEEP SELECTED', onclick="$('#loadpage').show(); $('#divPageContent').hide();", css_class='btn btn-primary btn-form')
                    Submit('submit', 'KEEP SELECTED SAMPLES', onclick = "keepSelected()", css_class='btn btn-primary btn-form'),

                    Submit('submit', 'REMOVE SELECTED SAMPLES', onclick="removeSelected()", css_class='btn btn-primary btn-form'),

                    Submit('submit', 'PROCEED WITH ALL SAMPLES', onclick="$('#loadpage').show(); $('#divPageContent').hide();proceed()", css_class='btn btn-primary btn-form'),

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

    def make_query(self,cleaned_data,query_id,old_query):


        hiddenString = str(cleaned_data.get("hiddenIDs"))
        hiddenList = hiddenString.split(",")
        if hiddenList[-1] == "keep":
            cleanList = [x for x in hiddenList if x not in ["keep", "proceed","remove"]]
            queryString = ",".join(cleanList)
            # success_url = reverse_lazy("samples") + "pick/" + query_id
            success_url = reverse_lazy("bench") + "pick/" + query_id

        if hiddenList[-1] == "remove":
            removeString = ",".join(hiddenList[:-1])
            removeList = removeString.split(",")
            success_url = reverse_lazy("bench") + "pick/" + query_id
            with open(os.path.join(DATA_FOLDER,"queryData",old_query,"query.txt"), 'r') as queryfile:
                old_SRX_string = queryfile.read()
            old_list = old_SRX_string.split(",")
            new_list = [x for x in old_list if x not in removeList]
            cleanList = [x for x in new_list if x not in ["keep", "proceed", "remove"]]
            queryString = ",".join(cleanList)

        if hiddenList[-1] == "proceed":
            success_url = reverse_lazy("bench") + query_id
            with open(os.path.join(DATA_FOLDER, "queryData", old_query, "query.txt"), 'r') as queryfile:
                queryString = queryfile.read()


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
        return(query_id,call,success_url)
    def start_query(self,old_query):
        query_id = self.generate_id()
        return self.make_query(self.cleaned_data,query_id, old_query)