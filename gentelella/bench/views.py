from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
#from miRNA.models import Micro
from django.views.generic import DetailView
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT, MICROS_FOLDER, SUB_SITE
import os
from study.summary_plots import makeMirBox
from bench.forms import BenchForm
from django.views.generic import FormView
from samples.forms import SamplesForm
from app.models import Sample
import json

# Create your views here.

# class Bench(FormView):
#     template_name = 'app/samples.html'
#     form_class = BenchForm
#     def get_context_data(self, **kwargs):
#         context = super(FormView, self).get_context_data(**kwargs)

class StartSample(FormView):
    template_name = 'app/samples.html'
    form_class = SamplesForm
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Select samples from the database:'
        samples = Sample.objects.all()
        table_data = []
        # qs = list(samples.values_list('Healthy', 'Cancer', 'Desc', 'Fluid', 'Sex'))
        # df = pd.DataFrame.from_records(qs)
        # print(df)
        for sam in samples:
            organism = sam.Organism
            SRP = sam.SRP
            SRX = sam.Experiment
            Library = sam.Library
            BIOS = sam.Sample
            instrument = sam.Instrument
            sex = sam.Sex
            fluid = sam.Fluid
            extraction = sam.Extraction
            healthy = sam.Healthy
            cancer = sam.Cancer
            exosome = sam.Exosome
            desc = sam.Desc
            table_data.append(
                #[SRP,SRX, BIOS, organism, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
                [SRP,SRX, BIOS, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])

        js_data = json.dumps(table_data)
        #print(js_data)
        context["data"] = js_data

        return context
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.clean()
        query_id, call = form.start_query()
        self.success_url = SUB_SITE+"/bench/" + query_id
        os.system(call)

        return super(StartSample, self).form_valid(form)


class BenchSample(FormView):
    template_name = 'app/samples_query.html'
    form_class = BenchForm
    query_id = ""

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        query_id = str(self.request.path_info).split("/")[-1]
        #content_folder = os.path.join(MEDIA_ROOT, query_id, "queryOutput")
        content_folder = os.path.join(DATA_FOLDER, "queryData",query_id, "queryOutput")
        with open(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt"), 'r') as queryfile:
            SRX_string = queryfile.read()
        samples_ids = SRX_string.split(",")
        #print(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt"))
        #print(os.path.exists(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt")))
        #print(SRX_string)
        context['SRX_string'] = SRX_string
        samples_ids = list(filter(None, samples_ids))
        context['pagetitle'] = str(len(samples_ids)) + ' samples selected'
        samples = Sample.objects.all().filter(Experiment__in=samples_ids)
        table_data = []
        for sam in samples:
            SRP = sam.SRP
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
            exosome = sam.Exosome
            desc = sam.Desc
            table_data.append(
                [SRP, SRX, BIOS, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
        js_data = json.dumps(table_data)
        # print(js_data)
        context["data"] = js_data
        return context

    def form_valid(self, form,**kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        context = super(FormView, self).get_context_data(**kwargs)
        old_query = str(self.request.path_info).split("/")[-1]
        form.clean()
        #old_query = query_id
        #input_query =
        query_id, call = form.start_DE(old_query)
        self.success_url = SUB_SITE+"/bench/compare/" + query_id
        print(call)
        return super(BenchSample, self).form_valid(form)

class BenchCompare(FormView):
    template_name = 'app/samples_query.html'
    form_class = BenchForm

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        query_id = str(self.request.path_info).split("/")[-1]
        #content_folder = os.path.join(MEDIA_ROOT, query_id, "queryOutput")
        content_folder = os.path.join(DATA_FOLDER, "queryData",query_id, "queryOutput")
        # with open(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt"), 'r') as queryfile:
        #     SRX_string = queryfile.read()
        # samples_ids = SRX_string.split(",")
        #print(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt"))
        #print(os.path.exists(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt")))
        #print(SRX_string)
        # context['SRX_string'] = SRX_string
        # samples_ids = list(filter(None, samples_ids))
        context['pagetitle'] = str(len(samples_ids)) + ' samples selected'
        samples = Sample.objects.all().filter(Experiment__in=samples_ids)
        table_data = []
        for sam in samples:
            SRP = sam.SRP
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
            exosome = sam.Exosome
            desc = sam.Desc
            table_data.append(
                [SRP, SRX, BIOS, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
        js_data = json.dumps(table_data)
        # print(js_data)
        context["data"] = js_data
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.clean()
        query_id, call = form.start_query()
        self.success_url = SUB_SITE+"/bench/compare/" + query_id
        os.system(call)

        return super(BenchCompare, self).form_valid(form)


def bench(request):
    context = dict()
    query_id = str(request.path_info).split("/")[-1]
    context["pagetitle"] = "Compare selected Dataset with sRNAbench jobs"
    #table_cols = ["miRNA", "Browse miRNA data"]
    template = loader.get_template('app/bench.html' )
    return HttpResponse(template.render(context, request))

# Create your views here.
