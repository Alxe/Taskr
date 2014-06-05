__author__ = 'Alej. N. Pérez'

from django.conf import settings
from django.views.generic.base import RedirectView
from django.contrib.auth import logout


class LogoutView(RedirectView):
    """ Class-based view to logout existing users, if any """
    permanent = False
    url = getattr(settings, 'ACCOUNTS_NEXT_LOGOUT', '/')

    def get(self, request, *args, **kwargs):
        """ Handles GET requests, logging an user out and redirecting to a url """
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
