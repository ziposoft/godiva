#!/usr/bin/env python

import sys,os
import csv,re
import django
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "godiva_web.settings.development")
from django.contrib.auth.models import User
from track.models import *
django.setup() #this is required!
from profiles.signals import *
import re

a = re.compile("^([A-Z][0-9]+)*$")
re_seconds = re.compile("^(?P<sec>[0-9]+)(\.(?P<tenths>[0-9]))?$")
re_time = re.compile("^(?P<min>[0-9]+):(?P<sec>[0-9][0-9])$")
re_time_bad = re.compile("^(?P<min>[0-9]+):(?P<sec>[0-9][0-9]):00$")


def testregex(text):
    print "testing matches"
    if re_seconds.match(text):
        print "matches re_seconds"
    m = re_time.match(text)
    if m:
        print "matches re_time %s %s" % (m.group('min'), m.group('sec'))
    m= re_time_bad.match(text)
    if m:
        print "matches re_time_bad"+m.group(1)

def bad_chars(tested_string):
    match = re.match("^[a-z.-]+$", tested_string)
    return match is None

def bad_name(tested_string):
    if bad_chars(tested_string):
        print "invalid name \"" + tested_string + "\""
        return True
    return False

def import_member_row(row, commit):
    for key, value in row.iteritems():
        row[key]=value.lower()

    if bad_name(row['name_first']):
        return False
    if bad_name(row['name_last']):
        return False

    un=row['name_last'] +  "." +row['name_first']
    try:
        user_list=User.objects.filter(username=un)
        if len(user_list)>1 :
            print "Multiple users with same username?"
            exit(1)
        if len(user_list) == 0:
            theuser = User.objects.create_user(un,row['email'],"godiva")
        else:
            theuser=user_list[0]

        theuser.last_name=row['name_last']
        theuser.first_name=row['name_first']
        theuser.email=row['email']
        theuser.save()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return False


    print(row['name_last'], row['name_first'])


def import_result_row(row,commit):

    minutes=0
    seconds=0
    seconds_tenths=0

    for key, value in row.iteritems():
        row[key]=value.lower().strip()

    if bad_name(row['name_first']):
        return False
    if bad_name(row['name_last']):
        return False

    t_in= row['time']


    m = re_seconds.match(t_in)
    if m:
        if(m.group('tenths')):
            seconds_tenths=int(m.group('tenths'))
        seconds= int(m.group('sec'))
    else:
        m = re_time_bad.match(t_in)
        if not m:
            m = re_time.match(t_in)
        if m:
            minutes = int(m.group('min'))
            seconds = int(m.group('sec'))
        else:
            print "bad time format:"+t_in
            return False

    result_time = timedelta(minutes=minutes, seconds=seconds,milliseconds=seconds_tenths*100)

    #print "%s = %d %d %d" % (t_in, minutes, seconds, seconds_tenths)


    #print(str(row))
    try:
        runners=Runner.objects.filter(
            name_last=row['name_last'],name_first=row['name_first'],gender=row['gender']
        )
        if len(runners)>1 :
            print "Multiple users with same username?"
            exit(1)
        if len(runners) == 0:
            print "not found, adding..."
            runner = Runner( name_last=row['name_last'],name_first=row['name_first'], gender=row['gender'])
            runner.save()
        else:
            runner=runners[0]


        day=datetime.datetime.strptime(row['date'], "%m/%d/%Y").date()

        sea,created=Season.objects.get_or_create(year=day.year)

        night, created =Night.objects.get_or_create(season=sea,date=day)
        try:
            # evt, created =EventType.objects.get_or_create(name=row['event'])
            evt =EventType.objects.get(name__iexact=row['event'])
        except Exception as e:
            print "Unknown event:'%s'" %  row['event']
            return False

        ev,created=Event.objects.get_or_create(type=evt,night=night)
        rslt,created=Result.objects.get_or_create(event=ev,runner=runner)
        rslt.age_at_time=row['age']
        rslt.time= result_time
        rslt.save()

    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return False


    #print(row['name_last'], row['name_first'])





def members(file, commit):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            import_member_row(row, commit)

def results(file, commit):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            import_result_row(row, commit)







if __name__ == "__main__":
    argc=len(sys.argv)

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    if(argc<2):
        print "please specify command"
        exit()
    if(argc<3):
        print "please specify csv file"
        exit()

    if (argc < 4):
        print "please specify 'test' or 'commit'"
        exit()

    func=locals()[sys.argv[1]]
    commit=(sys.argv[3] == 'commit')
    func(sys.argv[2], commit)



