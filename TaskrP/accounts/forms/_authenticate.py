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
        """ Return true if and only if the user exists, it's passwords match and it's not disabled. """
        cleaned_data = super(AuthenticationForm, self).clean()
        email = cleaned_data['email']
        password = cleaned_data['password']
        if not self._is_user_valid(email, password):
            raise forms.ValidationError(self._error_messages['authentication_failed'], code='authentication_failed')
        return cleaned_data

    def _is_user_valid(self, email, password):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return True
        except User.DoesNotExist:
            pass
        return False