
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpRequest
from app.models import Sample
from django.views.generic import FormView
from samples.forms import SamplesForm
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT, MEDIA_URL
from study.summary_plots import makeGenomePlot, makeTop20, makePie10,makeSpeciesPlot,makeTop20CV,makeBottom20CV,makeDEbox
from study.views import sortedMatrixToTableList
# Create your views here.
import json
import os
from app.datatable import create_datatable
from django.core.urlresolvers import reverse_lazy
import subprocess


def create_table(head, body, table_id = "datatable", table_class = "table table-striped table-bordered dataTable no-footer"):
	'''
	Input:
		header	columns names (list; tuple)
		body	rows (list of lists; tuple of tuples; list of tuples)
		(optional) table_id	table ID (default: "datatable"; string)
		(optional) table_class	table class (default: "table table-striped table-bordered dataTable no-footer"; string)
	Output:
		HTML DataTable (string)
	'''
	assert any([isinstance(head, list), isinstance(head, tuple)])
	assert any([isinstance(body, list), isinstance(body, tuple)])
	col_template = '<th>{col}</th>'

	row_template = '<tr>{cols}</tr>'.format(cols = "<td>{}</td>" * len(head))
	head = '\n'.join(['<tr>'] + list(map(lambda col: col_template.format(col = col), head)) + ['</tr>'])
	body = '\n'.join(list(map(lambda row: row_template.format(*row), body)))
	html_table = '''<table id="{table_id}" class="{table_class}">
	<thead>\n{head}\n</thead>
	<tbody>\n{body}\n</tbody>
	</table>'''.format(table_id = table_id, table_class = table_class, head = head, body = body)
	return html_table


def samples_table(request):
    context = {}
    template = loader.get_template('app/samples.html')
    # studies = Study.objects.all()
    # samples = Sample.objects.all()
    #
    # total = len(studies)
    # recent = Study.objects.all()[total-6:total-1]
    #print(len(recent))
    results = dict()
    samples = Sample.objects.all()
    table_data = []
    #qs = list(samples.values_list('Healthy', 'Cancer', 'Desc', 'Fluid', 'Sex'))
    #df = pd.DataFrame.from_records(qs)
    # print(df)
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
        exosome = sam.Exosome
        desc = sam.Desc
        checkbox = "<input type='checkbox' id='" + sam.Experiment + "_check" + "'>"
        table_data.append(
            [SRX, BIOS, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
            #[SRX, BIOS, organism, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
    # context['pagetitle'] = str(study.SRP)

    js_data = json.dumps(table_data)
    print(js_data)
    results["data"] = js_data

    # for i,obj in enumerate(recent):
    #     SRP = obj.SRP
    #     title = obj.Title
    #     results["title"+str(i)] = "<a href='/study/"+ SRP + "'><b>" +title + "</b></a>"
    #     abstract = obj.Abstract
    #
    #     if len(abstract) < 499:
    #         results["abstract"+str(i)] = abstract
    #     #print(len(obj.Abstract))
    #     else:
    #         results["abstract" + str(i)] = abstract[0:499]+ "[...]<a href='/study/"+ SRP + "'><b> Read More </b></a>"
    #
    #
    #     results["srp"+str(i)] = SRP
    #     results["paper"+str(i)] = obj.Url
    #
    # #print(studies_ids)
    # print(len(studies))
    # results["samples"] = len(samples)
    # results["studies"]=len(studies)
    # results["fluids"] = len(set(Sample.objects.values_list('Fluid')))
    # print(results["fluids"])
    # #print(studies)
    context=results
    return HttpResponse(template.render(context, request))

class StartSample(FormView):
    template_name = 'app/samples.html'
    form_class = SamplesForm
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context['pagetitle'] = 'Select your samples:'
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
            checkbox = "<input type='checkbox' id='" + sam.Experiment + "_check" + "'>"
            desc = sam.Desc
            table_data.append(
                #[SRP,SRX, BIOS, organism, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
                #[checkbox,SRP,SRX, BIOS, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
                [checkbox,SRP,SRX, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])

        js_data = json.dumps(table_data)
        #print(js_data)
        context["data"] = js_data

        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        form.clean()

        query_id, call = form.start_query()
        self.success_url = reverse_lazy("samples") + query_id
        #self.success_url = "/samples/" + query_id
        #success_url = reverse_lazy("mirconstarget")
        os.system(call)

        return super(StartSample, self).form_valid(form)
    #success_url = reverse_lazy("BENCH")

    #return super(StartSample, self).form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     request.POST._mutable = True
    #     #print(SPECIES_PATH)
    #     request.POST['species'] = request.POST['species_hidden'].split(',')
    #     print(request.POST['species'])
    #     print(request.POST['species_hidden'].split(','))
    #     request.POST._mutable = False
    #     return super(Bench, self).post(request, *args, **kwargs)
    #
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #
    #     form.clean()
    #
    #     call, pipeline_id = form.create_call()
    #     self.success_url = reverse_lazy('srnabench') + '?id=' + pipeline_id
    #
    #     print(call)
    #     os.system(call)
    #     js = JobStatus.objects.get(pipeline_key=pipeline_id)
    #     js.status.create(status_progress='sent_to_queue')
    #     js.job_status = 'sent_to_queue'
    #     js.save()
    #     return super(StartSample, self).form_valid(form)


class SampleQuery(FormView):
    #print(self.request)
    template_name = 'app/samples_query.html'
    form_class = SamplesForm
    #post_dict = HttpRequest.POST
    post_dict = HttpRequest.POST
    import json
    with open('/opt/liqDB/liqDB/gentelella/queryData/post.json', 'w') as fp:
        json.dump(post_dict, fp)

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
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

        if len(SRX_string)<1:
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
        #(["relative_zip", "query_download.zip", ])

            # subprocess.Popen(["zip", os.path.join(content_folder, "miRNA_RPMadjLib.txt.zip"),
            #                   os.path.join(content_folder, "miRNA_RPMadjLib.txt")])
            # subprocess.Popen(["zip", os.path.join(content_folder,"miRNA_RCadj.txt.zip"), os.path.join(content_folder,"miRNA_RCadj.txt")])


        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        form.clean()

        query_id, call = form.start_query()
        self.success_url = reverse_lazy("samples") + query_id
        os.system(call)

        return super(SampleQuery, self).form_valid(form)
    #success_url = reverse_lazy("BENCH")

    #return super(StartSample, self).form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     request.POST._mutable = True
    #     #print(SPECIES_PATH)
    #     request.POST['species'] = request.POST['species_hidden'].split(',')
    #     print(request.POST['species'])
    #     print(request.POST['species_hidden'].split(','))
    #     request.POST._mutable = False
    #     return super(Bench, self).post(request, *args, **kwargs)
    #
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #
    #     form.clean()
    #
    #     call, pipeline_id = form.create_call()
    #     self.success_url = reverse_lazy('srnabench') + '?id=' + pipeline_id
    #
    #     print(call)
    #     os.system(call)
    #     js = JobStatus.objects.get(pipeline_key=pipeline_id)
    #     js.status.create(status_progress='sent_to_queue')
    #     js.job_status = 'sent_to_queue'
    #     js.save()
    #     return super(StartSample, self).form_valid(form)