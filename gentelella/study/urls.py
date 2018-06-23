from study import views

from django.conf.urls import url

urlpatterns = [
    #url(r'(<SRP>[A-Za-z0-9]+)', views.DisplayStudy.as_view())
    url(r'^(?P<SRP>[A-za-z0-9]+)', views.DisplayStudy.as_view())
]

