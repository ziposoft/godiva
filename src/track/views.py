

import zs.views

import django_tables2 as tables
import track.models as track_models
from django_tables2   import RequestConfig
from django_tables2.utils import A  # alias for Accessor
from django.shortcuts import render
from datetime import timedelta
TrackGenViews = zs.views.GenView(track_models)


class ColumnTime(tables.Column):
    def render(self, value):
        s=""

        ts= value.total_seconds()
        hours=int(ts/3600)
        minutes=int((ts%3600)/60)
        sec=int(ts%60)
        if hours>0:
            s= "%d:%.2d:%.2d" % (hours,minutes,sec)
        else:
            if minutes>0:
                s= "%d:%.2d" % ( minutes, sec)
            else:
                s="%d" % sec


        if value.microseconds :
            s= s+"."+ str(value.microseconds/100000)
        return s

class TableRunners(tables.Table):
    name_first = tables.Column(verbose_name="First Name")
    name_last = tables.LinkColumn('track:runner',args=[A('id')])
    gender = tables.Column(verbose_name="Gender")
    result_count=tables.Column( accessor='result_count',orderable=False,#need to figure out how to do this
                                verbose_name="Number of results")

    def render_gender(self,value):
        return value #value.count()


    class Meta:
        #model = Runner
        attrs = {"class": "paleblue"}

class TableResults(tables.Table):
    date= tables.Column(verbose_name="Date",accessor='event.night.date')
    event= tables.Column(accessor='event.type')
    runner = tables.Column(verbose_name="Runner")
    age = tables.Column(verbose_name="Age",accessor='age_at_time')
    time = ColumnTime(accessor="time")

    class Meta:
        #model = Result
        attrs = {"class": "paleblue"}
        exclude = {"id"}





def events(request):
    table = TableRunners(track_models.Runner.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'track/table.html', {'table': table})


def runners(request):
    table = TableRunners(track_models.Runner.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'track/table.html', {'table': table})

def runner(request,slug):
    therunner=track_models.Runner.objects.get(id=slug)
    table = TableResults(track_models.Result.objects.filter(runner__id=slug),exclude={'runner','age','age_at_time'})
    RequestConfig(request).configure(table)
    return render(request, 'track/runner.html', {'table': table,'theruner': therunner})






class TrackTableViewEvents(tables.Table):
    age_at_time = tables.Column(verbose_name="Age")

    class Meta:
        model = track_models.EventType

class TrackTableView(tables.Table):
    age_at_time = tables.Column(verbose_name="Age")

    class Meta:
        model = track_models.Result

def index(request):
    return TrackGenViews.index(request)

def ResultList(request):
    #return render(request, "track/results_list.html", {"results": track_models.Result.objects.all()})
    table = TableResults(track_models.Result.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'track/table.html', {'table': table})

