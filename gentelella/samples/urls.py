from samples import views

from django.conf.urls import url

urlpatterns = [
    #url(r'(<SRP>[A-Za-z0-9]+)', views.DisplayStudy.as_view())
    url(r'^', views.StartSample.as_view())
    # url(r'^', views.samples_table)
]

