from bench import views

from django.conf.urls import url

urlpatterns = [
    #url(r'(<SRP>[A-Za-z0-9]+)', views.DisplayStudy.as_view())

    # url(r'^compare/(?P<query_id>[A-za-z0-9]+)', views.BenchCompare.as_view()),
    url(r'^compare/(?P<query_id>[A-za-z0-9]+)', views.bench),
    url(r'^(?P<query_id>[A-za-z0-9]+)', views.BenchSample.as_view()),
    url(r'^',views.StartSample.as_view() )

]

