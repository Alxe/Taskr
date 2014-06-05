__author__ = 'Alex'

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from ..models import User


class RegistrationForm(forms.ModelForm):
    """ Form that creates an user with a given password """
    # Form fields
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    # Information dictionary about errors
    _error_messages = {
        'duplicate_email': _("An user with that email already exists."),
        'password_mismatch': _("The password fields didn't match."),
    }

    # Form metadata
    class Meta:
        """ Form metadata """
        model = User
        fields = ['email', 'password1', 'password2']

    # Form validation methods
    # Called dynamically because of 'clean_{field}' convention
    def clean_email(self):
        """ Validates email, checking if it already exists in the database """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self._error_messages['duplicate_email'],
                                    code='duplicate_email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self._error_messages['password_mismatch'],
                                        code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user