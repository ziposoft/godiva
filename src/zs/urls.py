from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
   url(r'^(?P<table_name>[a-zA-Z0-9-.]+)/$', views.table_generic, name='detail'),
]
