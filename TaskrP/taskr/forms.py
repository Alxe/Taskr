from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from taskr.models import TaskrUser, Task

class TaskrUserCreationForm(UserCreationForm):
    email = forms.EmailField(help_text=u'Your login credential. No spam, we promise!')
    password1 = forms.CharField(help_text=u'At least five alphanumeric characters.', min_length=5, widget=forms.PasswordInput)

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']


class TaskrUserLoginForm(forms.Form):
    email = forms.EmailField(help_text=u'')
    password = forms.CharField(help_text=u'', min_length=5, widget=forms.PasswordInput)


class TaskCreationForm(forms.ModelForm):
    title = forms.CharField(help_text=u'')
    deadline = forms.DateTimeField(help_text=u'Optional, format: yyyy/mm/dd (HH:MM)')
