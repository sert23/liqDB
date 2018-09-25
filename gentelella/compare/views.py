from django.shortcuts import render

from django.views.generic import FormView, TemplateView
from app.models import Sample
import json
import os
from compare.forms import CompareForm, ManualForm
from django.core.urlresolvers import reverse_lazy
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT, SUB_SITE, MEDIA_URL, PATH_TO_RSCRIPT, HM_SCRIPT
from study.views import sortedMatrixToTableList
from study.summary_plots import makeGenomePlot, makeTop20, makePie10,makeSpeciesPlot,makeTop20CV,makeBottom20CV,makeDEbox,makeDEbox_pval
import subprocess
# Create your views here.

class StartCompare(FormView):
    template_name = 'app/samples.html'
    form_class = CompareForm
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Select your sets of samples:'
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
        self.success_url = reverse_lazy("datasets") + "pick/" +query_id
        #self.success_url = "/samples/" + query_id
        #success_url = reverse_lazy("mirconstarget")
        #os.system(call)
        return super(StartCompare, self).form_valid(form)
    #success_url = reverse_lazy("BENCH")

class PickCompare(FormView):
    template_name = 'app/compare_pick.html'
    form_class = ManualForm
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        query_id = str(self.request.path_info).split("/")[-1]
        #content_folder = os.path.join(MEDIA_ROOT, query_id, "queryOutput")
        content_folder = os.path.join(DATA_FOLDER, "queryData",query_id, "queryOutput")
        with open(os.path.join(DATA_FOLDER,"queryData",query_id,"query1.txt"), 'r') as queryfile:
            SRX_string1 = queryfile.read()

        with open(os.path.join(DATA_FOLDER,"queryData",query_id,"query2.txt"), 'r') as queryfile:
            SRX_string2 = queryfile.read()
        # with open(os.path.join(content_folder,), 'r') as exp_file:
        #     exp_data = [[n for n in line.split()] for line in exp_file.readlines()]

        #first table
        samples_ids = SRX_string1.split(",")
        samples_ids = list(filter(None, samples_ids))
        #context['pagetitle'] = str(len(samples_ids)) + ' samples selected'
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
            checkbox = "<input type='checkbox' value='" + sam.Experiment + "' name='to_list'>"
            RC = sam.RC
            desc = sam.Desc
            table_data.append(
                [checkbox, SRP, SRX, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc, RC])
        js_data = json.dumps(table_data)
        # print(js_data)
        context["data"] = js_data

        #second table
        samples_ids = SRX_string2.split(",")
        samples_ids = list(filter(None, samples_ids))
        # context['pagetitle'] = str(len(samples_ids)) + ' samples selected'
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
            checkbox = "<input type='checkbox' value='" + sam.Experiment + "' name='to_list2'>"
            RC = sam.RC
            desc = sam.Desc
            table_data.append(
                [checkbox, SRP, SRX, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc, RC])
        js_data = json.dumps(table_data)
        # print(js_data)
        context["data2"] = js_data


        if len(SRX_string1)<2 and len(SRX_string2)<2:
            context['pagetitle'] = 'Sorry, no samples matched your query'
            return context

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.clean()
        query_id, call = form.start_query()
        self.success_url = reverse_lazy("datasets") + query_id
        #self.success_url = "/samples/" + query_id
        #success_url = reverse_lazy("mirconstarget")
        os.system(call)
        return super(PickCompare, self).form_valid(form)
    #success_url = reverse_lazy("BENCH")


class CompareQueries(TemplateView):
    #print(self.request)
    template_name = 'app/compare_query.html'
    #form_class = SamplesForm
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        query_id = str(self.request.path_info).split("/")[-1]
        #content_folder = os.path.join(MEDIA_ROOT, query_id, "queryOutput")
        content_folder = os.path.join(DATA_FOLDER, "queryData",query_id, "queryOutput")
        with open(os.path.join(DATA_FOLDER,"queryData",query_id,"query.txt"), 'r') as queryfile:
            SRX_string = queryfile.read()
        # with open(os.path.join(content_folder,), 'r') as exp_file:
        #     exp_data = [[n for n in line.split()] for line in exp_file.readlines()]

        samples_ids = SRX_string.split(",")
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
        context['SRX_string'] = SRX_string
        #context['RNAcols'] = "hello"

        if len(SRX_string)<2:
            context['pagetitle'] = 'Sorry, no samples matched your query'
            return context

        RNAcols, RNAbody = sortedMatrixToTableList(os.path.join(content_folder, "RNAmaping_sort.txt"))
        MIRcols, MIRbody = sortedMatrixToTableList(os.path.join(content_folder, "miRNA_RCadj.txt"))
        context['RNAcols'] = RNAcols
        context['RNAbody'] = RNAbody
        context['MIRcols'] = MIRcols
        context['MIRbody'] = MIRbody

        #print(os.path.join(content_folder, "miRNA_RCadj.txt"))
        #context["exp_table"] = create_datatable(exp_data)

        plot = makeGenomePlot(os.path.join(content_folder, "RNAmaping_sort.txt"), "")
        top20 = makeTop20(os.path.join(content_folder, "miRNA_RPMadjLib_sort.txt"), "")
        toPie = makePie10(os.path.join(content_folder, "miRNA_RPMadjLib_sort.txt"))
        context["mapBox"] = plot
        context["top20"] = top20
        context["toPie"] = toPie
        context["speciesPlot"] = makeSpeciesPlot(os.path.join(content_folder, "genomeDistribution_sort.txt"))
        context["Gcols"], context["Gbody"] = sortedMatrixToTableList(os.path.join(content_folder, "genomeDistribution_sort.txt"))
        context["top20CV"] = makeTop20CV(os.path.join(content_folder, "miRNA_RPMadjLib_CV_min20.txt"))
        # context["bottom20CV"] = makeDEbox("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies/SRP062974/de/health_state/matrix_miRNA_RPMadjLib.txt")
        context["bottom20CV"] = makeBottom20CV(os.path.join(content_folder, "miRNA_RPMadjLib_CV_min20.txt"))

        context["RC_link"] = os.path.join(MEDIA_URL,  "queryData",query_id, "queryOutput", "miRNA_RCadj.txt.zip")
        context["RPM_link"] = os.path.join(MEDIA_URL, "queryData",query_id, "queryOutput", "miRNA_RPMadjLib.txt.zip")
        context["full_link"] = os.path.join(MEDIA_URL, "queryData",query_id, "queryOutput", "query_download.zip")

        #subprocess.Popen(["touch", os.path.join(content_folder,"query_download")], cwd="/opt/liqDB")
        if not os.path.exists(os.path.join(content_folder, "query_download.zip" )):
            subprocess.Popen(["/opt/liqDB/liqDB/gentelella/bin/relative_zip", "query_download.zip",  content_folder])
            subprocess.Popen(["zip", "miRNA_RPMadjLib.txt.zip" , "miRNA_RPMadjLib.txt"],cwd= content_folder)
            subprocess.Popen(["zip", "miRNA_RCadj.txt.zip" , "miRNA_RCadj.txt"],cwd= content_folder)
        initial_dir = os.path.join(content_folder, "de")
        DE_list = [name for name in os.listdir(initial_dir) if os.path.isdir(os.path.join(initial_dir, name))]
        DE_objs = []
        for comparison in DE_list:
            files = os.listdir(os.path.join(content_folder, "de", comparison))
            if os.path.exists(
                    os.path.join(content_folder, "de", comparison, "matrix_miRNA_RPMadjLib.txt").replace(
                            "\\", "/")):
                DE_table = os.path.join(content_folder, "de", comparison, "").replace("\\", "/")
                # DE_plot = makeDEbox(
                #     os.path.join(content_folder, "de", comparison, "matrix_miRNA_RPMadjLib.txt")).replace(
                #     "\\", "/")

                DE_file = [f for f in files if f.startswith("de_")][0]

                DE_plot = makeDEbox_pval(os.path.join(content_folder, "de", comparison, "matrix_miRNA_RPMadjLib.txt"),
                                         os.path.join(content_folder, "de", comparison, DE_file))

                HM_path = os.path.join(MEDIA_URL,  "queryData",query_id, "queryOutput", "de", comparison, "heatmap_euclidean.html")
                HM_link = "<a href='" + HM_path + "'><h3><b> See heatmap with hierarchical clustering </b><h3></a>"

                if not os.path.exists(os.path.join(MEDIA_ROOT,  "queryData",query_id, "queryOutput","de",comparison,"heatmap_euclidean.html")):
                    #output = ('temp.txt', 'w') as output:
                    #server = subprocess.Popen('./server.py', stdout=output)
                    #subprocess.Popen([PATH_TO_RSCRIPT, HM_SCRIPT, os.path.join(MEDIA_ROOT,  "queryData",query_id, "queryOutput","de",comparison)], ">",os.path.join(MEDIA_ROOT,  "queryData",query_id, "queryOutput","de",comparison,"Rlog.txt")])
                    print("lelo")
                DE_objs.append([comparison, DE_table, DE_plot, HM_link])
            else:
                DE_table = os.path.join(content_folder, "de", comparison, "").replace("\\", "/")
                DE_objs.append([comparison, DE_table, " ", " "])
                # print(os.path.join(studies_folder,study.SRP,"de",comparison,"matrix_miRNA_RPMadjLib.txt"))
        context["DE_list"] = DE_list
        context["DE_objs"] = DE_objs
        #(["relative_zip", "query_download.zip", ])

            # subprocess.Popen(["zip", os.path.join(content_folder, "miRNA_RPMadjLib.txt.zip"),
            #                   os.path.join(content_folder, "miRNA_RPMadjLib.txt")])
            # subprocess.Popen(["zip", os.path.join(content_folder,"miRNA_RCadj.txt.zip"), os.path.join(content_folder,"miRNA_RCadj.txt")])


        return context

