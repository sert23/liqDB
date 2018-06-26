from django.shortcuts import render

from django.views.generic import FormView
from django.views.generic import DetailView

from study.forms import StudyForm
from app.models import Study, Sample
import pandas as pd
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT
import os
# Create your views here.

class DisplayStudy(DetailView):

    model = Study

    #study = Study.objects.filter(SRP__exact=SRP)
    #print(ProcessFormView.request)
    slug_field='SRP'
    slug_url_kwarg = 'SRP'
    template_name = 'app/study.html'
    form_class = StudyForm
    # def get(self,**kwargs):
    #     request = super(FormView, self).get_context_data(**kwargs)

    #get_form_kwargs


    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        expression_mat = os.path.join(DATA_FOLDER,"SRP062974","RCadj_miRNA_sort.txt")
        exp_table = []
        print("hello")
        print(os.path.exists(os.path.join(MEDIA_ROOT)))
        with open(expression_mat) as matFile:
            lines = matFile.readlines()
            headerLine =lines.pop(0)
            for line in lines:
                fields = line.rstrip().split("\t")
                exp_table.append(fields)
        import json
        column_list = []
        for e in headerLine.rstrip().split("\t"):
            new_dict=dict()
            new_dict["title"] = e
            column_list.append(new_dict)
            #print(e)
        context["exp_columns"] = json.dumps(column_list)
        exp_data = json.dumps(exp_table)
        context["exp_data"] = exp_data
        #print(os.listdir(os.path.join(DATA_FOLDER,"SRP062974")))
        study = context.get('object')
        context['pagetitle'] = study.SRP
        SRP = study.SRP
        SRP_link = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/?study=' + SRP
        SRP_field = "<a href='" + SRP_link + "'><b> at SRA </b></a>"
        PRJ = study.PRJ
        PRJ_link = "https://www.ncbi.nlm.nih.gov/bioproject/" + PRJ
        PRJ_field = "<a href='" + PRJ_link + "'><b> BioProject </b></a>"
        context["title"] = study.Title
        context["Abstract"] = study.Abstract
        article = study.Url
        if article != "---":
            article_field = "<a href='" + article + "'><b> See Article</b></a>"
            context["article_field"] = article_field
        context["PRJ_field"] = PRJ_field
        context["SRP_field"] = SRP_field
        samples = Sample.objects.filter(SRP__exact=SRP)
        context["sample_number"] = len(samples)
        print(set(samples.values_list('Fluid',flat=True)))
        table_data = []
        qs = list(samples.values_list('Healthy', 'Cancer', 'Desc','Fluid','Sex'))
        df = pd.DataFrame.from_records(qs)
        #print(df)
        for sam in samples:
            organism = sam.Organism
            SRX = sam.Experiment
            Library = sam.Library
            BIOS = sam.Sample
            instrument = sam.Instrument
            sex = sam.Sex
            fluid = sam.Fluid
            extraction = sam.Extraction
            healthy = sam.Healthy
            cancer = sam.Cancer
            exosome= sam.Exosome
            desc = sam.Desc
            table_data.append([SRX, BIOS ,organism,instrument,sex,fluid,extraction,Library,healthy,cancer,exosome,desc])
        #context['pagetitle'] = str(study.SRP)

        js_data = json.dumps(table_data[0:1000])
        context["data"] = js_data
        SRX_list = list(samples.values_list('Experiment', flat=True))
        context["SRX_list"] = ",".join(SRX_list)
        # #print(type(js_data))

        return context

    # def render_to_response(self, context, **response_kwargs):
    #
    #     return super(JobStatusDetail, self).render_to_response(context, **response_kwargs)