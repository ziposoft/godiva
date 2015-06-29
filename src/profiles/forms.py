from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.layout = Layout( Field('name'),   )
       # self.helper.layout = Layout( Field('username'), Field('first_name'), Field('last_name'),   )

    class Meta:
        model = User
        #fields = ['name']
        fields = ['username','email','first_name','last_name']


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.add_input(Button('cancel', 'Cancel', css_class='btn-info', onclick="window.history.back()"))
        self.helper.layout = Layout(

            Field('picture'),
            Field('bio'),
            Submit('update', 'Update', css_class="btn-success"),
            Button('cancel', 'Cancel', css_class='btn-info', onclick="window.history.back()")
            #HTML("""<a class="btn btn-default" href="{% url 'personnel-index' %}">Cancel</a>"""),
            #Button('cancel', 'Cancel'),
            )

    class Meta:
        model = models.Profile
        fields = ['picture', 'bio']
