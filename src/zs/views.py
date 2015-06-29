from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
import sys
from django.http import HttpResponse
from django.template import RequestContext, loader
from . import models as data_models
import profiles.models
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from profiles.models import  Profile
import inspect
import logging
logger = logging.getLogger("project")


class classLinks:
    def __init__(self):
        self.list = []
    list = []

class classGeneric:
    def __init__(self):
        self.row = []
        self.links = []
    row = []
    links = []

class GenView:
    model_list = []

    def get_tables(self,module):
        #sys.path.append(str(module))
        #i = importlib.import_module(str(module)+".models")
        #i=__import__(str(module)+"/models.py")
        #from  models import *
        self.model_list = inspect.getmembers(module, inspect.isclass)
        logger.info(' get_tables'+str(len(self.model_list))+" "+str(module)+" "+str(type(module)))
        self.model_list.append( ("Users",  get_user_model()) )
        self.model_list.append( ("Profiles",  Profile) )


    def __init__(self, module):
        self.get_tables(module)



    def get_table(self,table_name):
        table = []
        fields = []

        if table_name in dict(self.model_list).keys():
            val = dict(self.model_list)[table_name]
        else:
            val = False

        return val

    def index(self,request,):
        tablelist = []
        for table in self.model_list:
            tablelist.append(table[0])

        template = loader.get_template('zs/table_list.html')
        context = RequestContext(request, {
            'tablelist': tablelist,
        })
        return HttpResponse(template.render(context))


    def table_generic(self,request, table_name):
        table_cl = self.get_table(table_name)
        table = []
        fields = []
        links=[]

        if (inspect.isclass(table_cl)):
            msg = ""
            fields=table_cl._meta.fields
            links = [rel.get_accessor_name() for rel in table_cl._meta.get_all_related_objects()]
            objlist=table_cl.objects.all()

            for obj in objlist:
                geno=classGeneric()
                table.append(geno)
                for f in fields:
                    data=getattr(obj,f.name)
                    geno.row.append(data)

                for link in links:
                    subtable=classLinks()
                    geno.links.append(subtable)
                    subobjs = getattr(obj, link).all()
                    for subobj in subobjs:
                        s=str(subobj)+ " "+str(type(subobj).__name__)
                        subtable.list.append(s)
        else:
            msg = "not found"



        template = loader.get_template('zs/table.html')
        context = RequestContext(request, {
            'msg': msg,
            'fields': fields,
            'links' : links,
            'table': table,
            'table_name': table_name,

        })
        return HttpResponse(template.render(context))
