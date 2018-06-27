from django.shortcuts import render

from django.views.generic import FormView
from django.views.generic import DetailView

from study.forms import StudyForm
from app.models import Study, Sample
import pandas as pd
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT
import os
from study.summary_plots import makeGenomePlot
# Create your views here.


def sortedMatrixToTableList(input_file):
    import json

    filename = input_file.split("/")[-1]
    last = False
    if "sort" in filename:
        last = True
    table_body =[]
    with open(input_file) as matFile:
        lines = matFile.readlines()
        headerLine = lines.pop(0)
        for line in lines:
            if last:
                tmp = line.rstrip().split("\t")[:-1]
                fields = [tmp[0]] +  [float(e) for e in tmp[1:]]
            else:
                fields = line.rstrip().split("\t")
            table_body.append(fields)
    column_list = []
    if last:
        header_fields = headerLine.rstrip().split("\t")[:-1]
    else:
        header_fields = headerLine.rstrip().split("\t")
    for e in header_fields:
        new_dict = dict()
        new_dict["title"] = e
        column_list.append(new_dict)
        # print(e)
    columns_json = json.dumps(column_list)
    body_json = json.dumps(table_body)
    print(len(column_list),len(table_body[0]))
    return columns_json, body_json
    #context["exp_data"] = exp_data


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
        studies_folder = "/opt/liqDB/liqDB/gentelella/data_folder/studies"
        #studies_folder = "C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies"
        study = context.get('object')
        context['pagetitle'] = study.SRP
        expression_mat = os.path.join(studies_folder,study.SRP,)
        expression_mat = os.path.join(DATA_FOLDER,"SRP062974","RCadj_miRNA.txt")
        RNAcols , RNAbody =sortedMatrixToTableList(os.path.join(studies_folder,study.SRP,"RNAmaping_sort.txt"))

        context['RNAcols'] = RNAcols
        context['RNAbody'] = RNAbody
        # with open("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/test/mapBox.html","r") as html_file:
        #     print(os.path.exists("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies/SRP062974/RCadj_miRNA_sort.txt"))
        plot = makeGenomePlot(os.path.join(studies_folder,study.SRP,"RNAmaping_sort.txt"), "")
            #plot2 = makeGenomePlot("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies/SRP062974/RNAmaping_sort.txt", "")
        context["mapBox"] = plot
            #context["mapBox2"] = plot2


        exp_table = []
        #print("hello")
        #print(os.path.exists(os.path.join(MEDIA_ROOT)))
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