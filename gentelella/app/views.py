from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from app.models import Study, Sample, StudiesTable
from app.pie_chart import pie_chart
from app.line_chart import line_chart
from app.bar_chart import year_bar_chart
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT, SUB_SITE
from django.views.generic import FormView
from app.forms import ContactForm
from django.core.urlresolvers import reverse_lazy
import os


def clean_upload():
    import time
    import shutil
    numdays = 86400 * 30
    now = time.time()
    #make white_list
    white_list=[]
    with open(os.path.join(MEDIA_ROOT,"white_list"), "r") as wfile:
        for line in wfile.readlines():
            white_list.append(line.rstrip())
    #get all folders in upload
    query_folder = os.path.join(MEDIA_ROOT,"queryData")

    folders = [x for x in os.listdir(query_folder) if os.path.isdir(os.path.join(query_folder,x))]

    to_rem = [os.path.join(query_folder,x) for x in folders if x not in white_list]
    with open("/opt/liqDB/liqDB/gentelella/data_folder/test1.txt", "w") as testfile1:
        testfile1.write(",".join(to_rem))

    with open("/opt/liqDB/liqDB/gentelella/data_folder/test.txt", "w") as testfile:
        for dir in to_rem:
            timestamp = os.path.getmtime(os.path.join(query_folder, dir))
            if now - numdays > timestamp:
                try:
                    testfile.write(dir+"\n")
                    # shutil.rmtree(os.path.join(query_folder,dir))  #uncomment to use
                except:
                    testfile.write("")




def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    studies = Study.objects.all()
    samples = Sample.objects.all()
    total = len(studies)
    recent = Study.objects.all()[total-6:total-1]
    #print(len(recent))
    results = dict()
    clean_upload()
    bar_years = dict()
    SRPs = set(Study.objects.all().values_list('SRP', flat=True))
    for sample in samples:
        SRP = sample.SRP
        if SRP in SRPs:
            year = sample.Date.year
            if SRP in bar_years:
                if year < bar_years[SRP]:
                    bar_years[SRP] = year
            else:
                bar_years[SRP] = year

    results["bar_years"] = year_bar_chart(list(bar_years.values()))
    # results["line_chart"] = line_chart(Sample)

    for i,obj in enumerate(recent):
        SRP = obj.SRP
        title = obj.Title
        results["title"+str(i)] = "<a href='"+SUB_SITE+"/study/"+ SRP + "'><b>" +title + "</b></a>"
        abstract = obj.Abstract

        if len(abstract) < 499:
            results["abstract"+str(i)] = abstract
        #print(len(obj.Abstract))
        else:
            results["abstract" + str(i)] = abstract[0:499]+ "[...]<a href='"+SUB_SITE+"/study/"+ SRP + "'><b> Read More </b></a>"
        results["srp"+str(i)] = SRP
        results["paper"+str(i)] = obj.Url
    #print(studies_ids)
    print(len(studies))
    results["samples"] = len(samples)
    results["studies"]=len(studies)
    fluid_list = Sample.objects.values_list('Fluid', flat=True)
    #print(len(fluid_list))
    fluid_list = [element for element in fluid_list if not "cell" in element]
    fluid_list = [element for element in fluid_list if not element == "NA"]

    #print(len(fluid_list))
    pie_string = pie_chart(fluid_list)

    results["fluid_chart"] =pie_string
    results["fluids"] = len(set(fluid_list))
    
    results["samples_data"], results["fluids_data"] = line_chart(Sample)
    
    print(results["fluids"])
    #print(studies)
    context=results
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    studies = Study.objects.all()
    #print(samples)
    total = len(studies)
    recent = Study.objects.all()[total - 6:total - 1]
    # print(len(recent))
    results = dict()
    for i, obj in enumerate(recent):
        results["title" + str(i)] = obj.Title
        results["abstract" + str(i)] = obj.Abstract
        results["srp" + str(i)] = obj.SRP
        results["paper" + str(i)] = obj.Url
    # print(studies_ids)
    #print(len(studies))
    results["studies"] = len(studies)
    # print(studies)
    context = results
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))



def studies(request):
    context={}
    studies = Study.objects.all()
    table_data = []
    for study in studies:
        #print(study.get("id"))
        SRP = study.SRP
        NS = len(Sample.objects.filter(SRP__exact=SRP))
        SRP_link = 'https://trace.ncbi.nlm.nih.gov/Traces/sra/?study=' + SRP
        SRP_field = "<a href='"+SRP_link+"'><b>"+SRP+"</b></a>"
        PRJ = study.PRJ
        PRJ_link = "https://www.ncbi.nlm.nih.gov/bioproject/" + PRJ
        PRJ_field = "<a href='" + PRJ_link + "'><b>" + PRJ + "</b></a>"
        Title = study.Title
        abstract = study.Abstract
        if len(abstract) < 199:
            Abstract = abstract
        #print(len(obj.Abstract))
        else:
            Abstract = abstract[0:199]+ "[...]<a href='"+SUB_SITE+"/study/"+ SRP + "'><b> Read More </b></a>"
        #Abstract = r'<button class="collapsible">Read more</button><div class="content"> <p>Abstract</p></div>'
        #Abstract = r'<button class="collapsible">Read more</button><div class="content"> <p>Abstract</p></div>'
        all_info=list(Sample.objects.filter(SRP__exact=SRP).values_list('Desc', flat=True))
        #print(set(all_info))
        Desc = ", ".join(set(all_info))
        prof = "<a href='"+SUB_SITE+"/study/" +SRP +"#tab_profile'><b> View Profiles </b></a>"
        #prof = PRJ_field
        #print(prof)
        #Abstract = study.Abstract
        table_data.append([SRP_field,PRJ_field,NS,Title,Abstract,Desc,prof])
    #studies = StudiesTable(queryset)

    # #context["data"]\
    # data= [["Tiger Nixon", "System Architect", "Edinburgh", "5421", "2011/04/25", "$320,800"],
    # ["Unity Butler", "Marketing of my Dick", "<a href='enlace'><b>link</b></a>", "5384", "2009/12/09", "$85,675"]]
    import json
    js_data = json.dumps(table_data)
    # #print(type(js_data))
    context["data"] = js_data

    #load_template = request.path.split('/')[-1]

    test_tag = "<thead>\n<tr>\n<th>Name</th>\n<th>Position2</th>\n<th>Office</th>\n<th>Age</th>\n<th>Start date</th>\n<th>Salary</th>\n</tr>\n</thead>"
    context["test_tag"] = test_tag
    #context["table"] = table
    #template = loader.get_template('app/tables_dynamic.html' )
    template = loader.get_template('app/studies_table.html' )
    # template = loader.get_template('app/bootstrap_table.html' )
    return HttpResponse(template.render(context, request))

class ContactView(FormView):
    template_name = 'app/samples.html'
    form_class = ContactForm
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.clean()
        form.send_email()
        #query_id, call = form.start_query()
        self.success_url = reverse_lazy("contact_success")
        #os.system(call)

        return super(ContactView, self).form_valid(form)

def success(request):
    context = dict()
    template = loader.get_template('app/success_contact.html')
    # template = loader.get_template('app/bootstrap_table.html' )
    return HttpResponse(template.render(context, request))

def about(request):
    context = dict()
    template = loader.get_template('app/about.html')
    # template = loader.get_template('app/bootstrap_table.html' )
    return HttpResponse(template.render(context, request))

def downloads(request):
    context = dict()
    template = loader.get_template('app/downloads.html')
    # template = loader.get_template('app/bootstrap_table.html' )
    return HttpResponse(template.render(context, request))


def make_table_div(input_file, title=" "):

    with open(input_file, 'r') as ifile:
        lines = ifile.readlines()

    headers = lines.pop(0)
    table_headers = []
    for header in headers.split("\t"):
        table_headers.append("<th>" + header.rstrip() +"</th>")
    table_body = []
    # lines.pop(0)
    for i,row in enumerate(lines):
        cells = row.split("\t")
        new_row =[]
        #new_row =['<tr><th scope="row">'+str(i)+'</th>']
        for cell in cells:
            new_row.append("<td>" + cell.rstrip() +"</td>")
        new_row.append("</tr>")
        table_body.append("".join(new_row))

    table_template = '''
                
                <div class="col-md-12 col-sm-12 col-xs-12">
          <div class="x_panel">
            <div class="x_title">
              <h2>{title}</h2>
              <div class="clearfix"></div>
            </div>
            <div class="x_content">

              <table class="table table-striped">
                <thead>
                  <tr>
                    {table_headers}
                  </tr>
                </thead>
                <tbody>
                  {table_body}
                </tbody>
              </table>

            </div>
          </div>
        </div>

        <div class="clearfix"></div>
    '''
    table_string = table_template.format(
        table_headers= "".join(table_headers),
        table_body = "".join(table_body),
        title = title
    )
    # return table_headers
    return table_string

def statistics(request):
    context = dict()
    template = loader.get_template('app/statistics.html')
    table_list = []
    with open(os.path.join(MEDIA_ROOT,"basic_statistics","desc.txt"),"r") as ifile:
        lines = ifile.readlines()
        for line in lines:
            list_of = line.split("\t")
            file = list_of[0]
            title = list_of[1]
            table_list.append(make_table_div(os.path.join(MEDIA_ROOT,"basic_statistics",file),title))

    context["table_list"] = table_list
    context["pagetitle"] = "Basic statistics"

    # template = loader.get_template('app/bootstrap_table.html' )
    return HttpResponse(template.render(context, request))