
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from app.models import Sample
from django.views.generic import FormView
from samples.forms import SamplesForm
# Create your views here.
import json

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
	col_template = '<th class="sorting" tabindex="0" aria-controls="datatable" rowspan="1" colspan="1" aria-sort="ascending" aria-label="{col}">{col}</th>'
	row_template = '<tr role="row">{cols}</tr>'.format(cols = "<td>{}</td>" * len(head))
	head = '\n'.join(['<tr role="row">'] + list(map(lambda col: col_template.format(col = col), head)) + ['</tr>'])
	body = '\n'.join(list(map(lambda row: row_template.format(*row), body)))
	html_table = '''<table id="{table_id}" class="{table_class}" role="grid" aria-describedby="datatable_info">
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
        table_data.append(
            [SRX, BIOS, organism, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
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
                [SRX, BIOS, organism, instrument, sex, fluid, extraction, Library, healthy, cancer, exosome, desc])
        # context['pagetitle'] = str(study.SRP)
        table_html = create_table(["Experiment","BioSample","Organism","Instrument","Sex","Fluid","Library preparation protocol",
                      "RNA Extraction protocol","Healthy","Cancer","Exosome isolation treatment","Sample info"],
                     table_data, "table_test"
                     )

        context["table_html"] = table_html



        js_data = json.dumps(table_data)
        print(js_data)
        context["data"] = js_data



        return context

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