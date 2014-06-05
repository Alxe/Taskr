__author__ = 'Alej. N. Pérez'

from ..forms import RegistrationForm
from django.conf import settings
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView


class RegisterView(CreateView):
    form_class = RegistrationForm
    success_url = getattr(settings, 'ACCOUNTS_REGISTER_NEXT', '/')
    template_name = None

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)