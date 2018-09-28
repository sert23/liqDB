from django.conf.urls import url, include
from app import views
#from study import urls

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^index.html$', views.index, name='index'),
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^studies', views.studies, name='studies'),
    url(r'^study/', include('study.urls')),
    url(r'^samples/', include('samples.urls')),
    url(r'^contact/', views.ContactView.as_view()),
    url(r'^mirna/', include('miRNA.urls')),
    url(r'^bench/', include('bench.urls')),
    url(r'^datasets/', include('compare.urls')),
    url(r'^success/', views.success, name="contact_success"),
    url(r'^about/', views.about),
    url(r'^downloads/', views.downloads),
    url(r'^statistics/', views.statistics),

    # The home page
    url(r'^$', views.index, name='index')
]