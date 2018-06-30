from miRNA import views

from django.conf.urls import url

urlpatterns = [
    #url(r'(<SRP>[A-Za-z0-9]+)', views.DisplayStudy.as_view())

    url(r'^(?P<pk>[0-9]+)', views.DisplayMicro.as_view()),
    url(r'^',views.search_mirna )

]

