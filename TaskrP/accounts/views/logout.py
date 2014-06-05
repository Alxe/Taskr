__author__ = 'Alej. N. Pérez'

from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.auth import logout


class LogoutView(RedirectView):
    permanent = False
    url = getattr(settings, 'ACCOUNTS_LOGOUT_NEXT', '/')

    def get(self, request, *args, **kwargs):
        """ Handles GET requests, logging an user out and redirecting to a url """
        # Log outs the user, if any
        logout(request)

        # Proceeds to redirect the
        return super(LogoutView, self).get(request, *args, **kwargs)
