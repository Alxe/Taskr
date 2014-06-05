from django import forms
from .models import Task


class TaskCreateForm(forms.ModelForm):
    title = forms.CharField(help_text=u'')
    deadline = forms.DateTimeField(help_text=u'Optional, format: yyyy/mm/dd (HH:MM)',
                                   widget=forms.DateTimeInput(attrs={'id': 'datepicker'}))

    class Meta:
        model = Task
        exclude = ['author', 'completed']
