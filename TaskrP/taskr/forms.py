from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from taskr.models import TaskrUser, Task


class TaskrUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = TaskrUser
        fields = ["email",]


class TaskrUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = TaskrUser


class TaskrUserLoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password', ]


class TaskCreationForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'deadline']
        exclude = ['pub_date', 'edit_date', 'completed', 'author']

