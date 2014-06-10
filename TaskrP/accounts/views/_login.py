__author__ = 'Alej. N. Pérez'

from ..forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView


class LoginView(FormView):
    """ Class-based view for user login purposes """
    form_class = AuthenticationForm
    template_name = None

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'next' in kwargs:
            self.success_url = kwargs['next']
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        if not self.success_url:
            self.success_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return self.success_url

    def form_valid(self, form):
        """ If form is valid, try to login user. If user can't be logged, form_invalid() will be called """
        user = authenticate(email=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        return self.form_invalid()