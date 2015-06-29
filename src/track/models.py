from django.db import models

# Create your models here.
from django.db import models
#from adaptor.model import CsvDbModel
#from django.core.validators import RegexValidator
from datetime import timedelta

CODE_MALE='m'
CODE_FEMALE='f'

CHOICES_GENDER = (
    (CODE_MALE, 'Male'),
    (CODE_FEMALE, 'Female'),
#this is for creating text: his, her, him, etc.
)


class Season(models.Model):
    year = models.SlugField(max_length=4)  # eg: 2015 .
    def __str__(self):
        return self.year


class Night(models.Model):
    season = models.ForeignKey(Season)
    date=models.DateField()
    type = models.CharField(max_length=40)
    def __str__(self):
        return str(self.date)




class EventType(models.Model):
    name = models.CharField(max_length=40, unique=True)
    distance_in_meters = models.FloatField(default=0)
    fixed_time = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Event(models.Model):
    type = models.ForeignKey(EventType)
    night = models.ForeignKey(Night)
    def __str__(self):
        return str(self.night) + " " + str(self.type)


class Runner(models.Model):
    name_first = models.CharField(max_length=40,blank=True)
    name_last = models.CharField(max_length=40,blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER,default=CODE_MALE)
    #num_results = models.PositiveIntegerField(default=0)

    @property
    def get_slug(self):
        return '{}.{}'.format(self.name_last ,self.name_first)

    @property
    def result_count(self):
        return self.result_set.count()

    def __str__(self):
        return self.name_first + " "+self.name_last


    class Meta:
       unique_together = (("name_first", "name_last"),)

    def save(self, *args, **kwargs):

        super(Runner, self).save(*args, **kwargs)


class Result(models.Model):
    runner = models.ForeignKey(Runner)
    age_at_time = models.PositiveIntegerField(default=0)
    event = models.ForeignKey(Event)
    time=models.DurationField(default=timedelta())
    @property
    def date(self):
        return self.event.night.date
    @property
    def event_type(self):
        return self.event.type

    def __str__(self):
        return str(self.event) + " "+str(self.time)


