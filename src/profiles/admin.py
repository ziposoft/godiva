from __future__ import unicode_literals
from django.contrib import admin
#from authtools.admin import NamedUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = Profile


class NewUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    #list_display = ('is_active', 'email', 'name', 'permalink', 'is_superuser', 'is_staff',)
    list_display = ('is_active', 'email', 'username', 'permalink', 'is_superuser', 'is_staff',)

    # 'View on site' didn't work since the original User model needs to
    # have get_absolute_url defined. So showing on the list display
    # was a workaround.
    def permalink(self, obj):
        un=obj.profile.user.username
        url = reverse("profiles:show",
                      kwargs={"slug": un})
        # Unicode hex b6 is the Pilcrow sign
        return '<a href="{}">{}</a>'.format(url, '\xb6')
    permalink.allow_tags = True


class MemberAdmin(Profile):
    #inlines = [UserProfileInline]
    #list_display = ('name_last', 'name_first', 'name',)
    list_display = ('name_last', 'name_first', 'username',)



#admin.site.unregister(User)
#admin.site.register(User, NewUserAdmin)
admin.site.register(Profile)
