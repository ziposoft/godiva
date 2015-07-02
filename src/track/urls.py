from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^g/$', views.index, name='index'),
    url(r'^$', views.TrackGenViews.index, name='home'),
    # url(r'^results/$', views.ResultList.as_view(), name='results'),
    url(r'^results/$', views.ResultList, name='results'),
    url(r'^events/$', views.events, name='events'),
    url(r'^runners/$', views.runners, name='runners'),
    url(r'^runner/(?P<slug>[a-zA-Z0-9-.]+)/$', views.runner, name='runner'),
    url(r'^year/$', views.ResultList, name='year'),
    # ex: /polls/5/
    # url(r'^g/(?P<table_name>[a-zA-Z0-9-.]+)/$', views.TrackGenViews.table_generic, name='detail'),
    url(r'^g/(?P<table_name>[a-zA-Z0-9-.]+)/$', views.TrackGenViews.dt_view, name='detail'),
    url(r'^g/(?P<table_name>[a-zA-Z0-9-.]+)/(?P<item>[0-9]+)/$', views.TrackGenViews.item_view, name='itemview'),
]
