from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from tinymce.models import HTMLField



class BaseProfile(models.Model):
    user = models.OneToOneField(#settings.AUTH_USER_MODEL,
                                User,
                                primary_key=True)

    #slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    picture = models.ImageField('Profile picture',
                                upload_to='profile_pics/%Y-%m-%d/',
                                null=True,
                                blank=True)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)
    name_first = models.CharField(max_length=80,blank=True)
    name_last = models.CharField(max_length=80,blank=True)
    bio2 = HTMLField()
    def get_full_name(self):
        return self.user.first_name+" "+self.user.last_name

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{}'s profile". format(self.user)
