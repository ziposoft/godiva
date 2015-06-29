
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from import_export.admin import ImportExportModelAdmin,ExportMixin
from import_export import fields,widgets
from import_export import resources
import logging
logger = logging.getLogger("project")


from .models import *
#
# class resPerson(resources.ModelResource):
#     class Meta:
#         model = Person
#         import_id_fields=['key_name']
#
# class admPerson(ImportExportModelAdmin):
#     list_display  = ('key_name', 'name_full')
#     resource_class=resPerson
#     pass

#admin.site.register(Person,admPerson)


def get_class_links(cl):
    #links = [rel.get_accessor_name() for rel in cl._meta.get_all_related_objects()]
    links = [rel.related_model for rel in cl._meta.get_all_related_objects()]

def get_class_subtable(cl):
    st_cl= type('subtable'+type(cl).__name__,(admin.TabularInline,),dict( dict(model=cl)))
    return st_cl

def get_class_res(cl):
    res_cl= type('res'+type(cl).__name__,(resources.ModelResource,),dict(
       Meta=type('Meta',(),dict(model=cl))))
    if hasattr(cl,'import_id_fields'):
        res_cl.import_id_fields=cl.import_id_fields
    return res_cl

def get_class_admin(cl):
    subtables = []
    links = [rel.related_model for rel in cl._meta.get_all_related_objects()]
    for link in links:
        subtables.append(get_class_subtable(link))

    adm_cl=type('admin'+type(cl).__name__,(ImportExportModelAdmin,),dict(
        resource_class=get_class_res(cl),inlines=subtables))
    adm_cl.list_display= [x.name for x in cl._meta.local_fields]
    return adm_cl

def register_admins(set):
    for cl in set:
        logger.info('admin register'+str(cl)+","+str(get_class_admin(cl)))
        admin.site.register(cl, get_class_admin(cl))


#admin.site.register(TrackSeason,TrackSeasonAdmin)
#register_admins([TrackEventType])


