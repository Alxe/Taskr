from django.contrib.auth import get_user_model

__author__ = 'Alex'

from ..models import User
from django import forms
from django.utils.translation import ugettext as _


class AuthenticationForm(forms.Form):
    """ Form that checks if an user can be logged in given a password """
    # Form fields
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Information dictionary about errors
    _error_messages = {
        'authentication_failed': _("Email and/or password provided are invalid."),
    }

    def clean(self):
        super(AuthenticationForm, self).clean()
        if not self.is_valid():
            raise forms.ValidationError(self._error_messages['authentication_failed'], code='authentication_failed')

    def is_valid(self):
        """ Return true if and only if the user exists, it's passwords match and it's not disabled. """
        if super(AuthenticationForm, self).is_valid():
            clean_email = self.cleaned_data['email']
            clean_password = self.cleaned_data['password']
            try:
                user = User.objects.get(email=clean_email)
                if user.check_password(clean_password) and user.is_active:
                    return True
            except User.DoesNotExist:
                pass
        return False

