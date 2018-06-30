from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from app.models import Study, Sample, StudiesTable
from app.pie_chart import pie_chart
from app.bar_chart import year_bar_chart


def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    studies = Study.objects.all()
    samples = Sample.objects.all()
    total = len(studies)
    recent = Study.objects.all()[total-6:total-1]
    #print(len(recent))
    results = dict()

    results["bar_years"] = year_bar_chart(["2009"]*6 + ["2012"]*10 + ["2018"]*5)

    for i,obj in enumerate(recent):
        SRP = obj.SRP
        title = obj.Title
        results["title"+str(i)] = "<a href='/study/"+ SRP + "'><b>" +title + "</b></a>"
        abstract = obj.Abstract

        if len(abstract) < 499:
            results["abstract"+str(i)] = abstract
        #print(len(obj.Abstract))
        else:
            results["abstract" + str(i)] = abstract[0:499]+ "[...]<a href='/study/"+ SRP + "'><b> Read More </b></a>"
        results["srp"+str(i)] = SRP
        results["paper"+str(i)] = obj.Url
    #print(studies_ids)
    print(len(studies))
    results["samples"] = len(samples)
    results["studies"]=len(studies)
    fluid_list = Sample.objects.values_list('Fluid', flat=True)
    pie_string = pie_chart(fluid_list)

    results["fluid_chart"] =pie_string
    results["fluids"] = len(set(fluid_list))
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
            Abstract = abstract[0:199]+ "[...]<a href='/study/"+ SRP + "'><b> Read More </b></a>"
        #Abstract = r'<button class="collapsible">Read more</button><div class="content"> <p>Abstract</p></div>'
        #Abstract = r'<button class="collapsible">Read more</button><div class="content"> <p>Abstract</p></div>'
        all_info=list(Sample.objects.filter(SRP__exact=SRP).values_list('Desc', flat=True))
        #print(set(all_info))
        Desc = ", ".join(set(all_info))
        prof = "<a href='/study/" +SRP +"#tab_profile'><b> View Profiles </b></a>"
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

