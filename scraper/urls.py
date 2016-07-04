from django.conf.urls import url, include
from . import views

app_name = 'scraper'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^output', views.output, name='output'),
]
