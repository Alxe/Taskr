from django import forms
from django.contrib.auth.models import User
from taskr.models import Task

class RegistrationForm(forms.ModelForm):
    pass

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'tag', 'author']
        exclude = ['pub_date', 'edit_date', 'completed', 'author']

