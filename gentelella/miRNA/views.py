from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from miRNA.models import Micro
from django.views.generic import DetailView
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT, MICROS_FOLDER,SUB_SITE
import os
from study.summary_plots import makeMirBox
#from django.core.mail import send_mail



# Create your views here.

def search_mirna(request):
    micros = Micro.objects.all()
    #micros_names = micros.values_list('name',flat=True)
    #print(list(micros_names))
    context = dict()
    context["pagetitle"] = "Search a miRNA:"
    #table_cols = ["miRNA", "Browse miRNA data"]
    table_body = []
    for m in micros:
        name = m.name
        pk = m.pk
        link_field = "<a href='"+SUB_SITE+"/mirna/" + str(pk) + "'><b> See data and graphs for this miRNA</b></a>"
        table_body.append([name, link_field])
    #context["tcols"] = table_cols
    context["tbody"] = table_body
    #load_template = request.path.split('/')[-1]
    template = loader.get_template('app/mirna_search.html' )


    # send_mail('My Subject', 'My message', 'liquiddbase@gmail.com',
    #           ['eaparicioeaparicio@gmail.com'], fail_silently=False)
    return HttpResponse(template.render(context, request))


class DisplayMicro(DetailView):

    model = Micro

    slug_field='pk'
    slug_url_kwarg = 'pk'
    template_name = 'app/mirna_search.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        # studies_folder = "/opt/liqDB/liqDB/gentelella/data_folder/studies"
        #studies_folder = STUDIES_FOLDER
        micro = context.get('object')
        miRNA = micro.name
        context['pagetitle'] = miRNA
        plot_list = []
        with open(os.path.join(MICROS_FOLDER,miRNA,"description.txt"), "r") as description:
            lines = description.readlines()
            for line in lines:
                target,title = line.split("\t")
                plot_list.append(makeMirBox(os.path.join(MICROS_FOLDER,miRNA,target),title))

        context["plot_list"] = plot_list

        return context

    #form_class = StudyForm