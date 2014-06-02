from django import forms
from django.contrib.auth.models import User
from taskr.models import Task


class RegisterForm(forms.ModelForm):

    def save(self):
        user = super(RegisterForm, self).save(commit=False)
        user.username = user.email
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password']


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'tag', 'author', 'deadline']
        exclude = ['pub_date', 'edit_date', 'completed', 'author']

