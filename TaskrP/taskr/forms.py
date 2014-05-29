from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.EmailField(max_length=30, widget=forms.TextInput(attrs=attrs_dict))
    password = forms.PasswordField()
    passwordConf = forms.PasswordField()
    # rest of the fields

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        passwordConf = cleaned_data.get("passwordConf")

        if(not len(User.objects.filter(username=username)) == 0):
            pass

        if(not str(password) == str(passwordConf)):
            pass

        # you can validate those here

    class Meta:
        model = User