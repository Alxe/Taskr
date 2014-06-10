from django import forms
from .models import Task


class TaskCreateForm(forms.ModelForm):
    title = forms.CharField(help_text=u'')
    deadline = forms.DateTimeField(help_text=u'Optional, format: yyyy/mm/dd (HH:MM)',
                                   widget=forms.DateTimeInput(attrs={'id': 'datepicker'}),
                                   required=False)

    class Meta:
        model = Task
        fields = ['title', 'deadline']


class TaskCompleteForm(forms.Form):
    id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    author_id = forms.IntegerField(required=True, widget=forms.HiddenInput())

    class Meta:
        fields = ['id', 'author_id']

    def is_valid(self):
        is_valid = super(TaskCompleteForm, self).is_valid()
        if is_valid:
            try:
                id = self.cleaned_data['id']
                author_id = self.cleaned_data['author_id']
                Task.objects.get(pk=id, author_id=author_id)
                return True
            except Task.DoesNotExist:
                pass
        return False
