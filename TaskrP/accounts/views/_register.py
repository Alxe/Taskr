from django.http.response import HttpResponseRedirect

__author__ = 'Alej. N. Pérez'

from ..forms import RegistrationForm
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView


class RegisterView(CreateView):
    """ Class-based view for registering users """
    form_class = RegistrationForm
    success_url = getattr(settings, 'ACCOUNTS_NEXT_REGISTER', '/')
    template_name = None

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """ Redirects if user is logged in, else continues normally """
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)
        return super(RegisterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """ After form is already valid, make sure to login user """
        response = super(RegisterView, self).form_valid(form)
        user = authenticate(email=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'])
        login(self.request, user)
        return response

