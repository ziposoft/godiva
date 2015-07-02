import django_tables2 as tables
from django_tables2   import RequestConfig
from django_tables2.utils import A  # alias for Accessor
from django.shortcuts import render
import inspect




class DtTemplate(tables.Table):
    #name_first = tables.Column(verbose_name="First Name")
    #name_last = tables.LinkColumn('track:runner',args=[A('id')])
    #gender = tables.Column(verbose_name="Gender")
    #result_count=tables.Column( accessor='result_count',orderable=False,verbose_name="Number of results")

    class Meta:
        #model = Runner
        attrs = {"class": "paleblue"}

