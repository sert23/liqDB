from django.shortcuts import render

from django.views.generic import FormView
from app.models import Sample
import json
import os
from compare.forms import CompareForm
from django.core.urlresolvers import reverse_lazy
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
        self.success_url = reverse_lazy("samples") + query_id
        #self.success_url = "/samples/" + query_id
        #success_url = reverse_lazy("mirconstarget")
        print(call)

        return super(StartCompare, self).form_valid(form)
    #success_url = reverse_lazy("BENCH")
