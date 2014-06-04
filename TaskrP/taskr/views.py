from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import MultipleObjectMixin, ListView
from taskr import models
from taskr.forms import TaskrUserCreationForm, TaskCreationForm, TaskrUserLoginForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('taskr:home'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class HomeView(CreateView, MultipleObjectMixin):
    # common
    model = models.Task
    template_name = 'home.html'

    #form
    form_class = TaskCreationForm
    success_url = '#'

    # list
    object_list = models.Task.objects.all()
    context_object_name = 'tasks'
    paginate_by = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('taskr:index'))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = super(HomeView, self).get_queryset()
        q.filter(author=get_user_model().objects.get(user=self.request.user))

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = get_user_model().objects.get(user=self.request.user)
        return super(HomeView, self).form_valid(form)


class TaskListView(ListView):
    queryset = models.Task.objects.filter(completed=False)
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        q = super(TaskListView, self).get_queryset()
        q.filter(author=self.request.user.id)
        return q


class TaskArchiveView(TaskListView):
    queryset = models.Task.objects.filter(completed=True)
    template_name = 'task_archive.html'


class TaskDetailView(DetailView):
    template_name = 'task_detail.html'
    queryset = models.Task.objects.filter(completed=False)


class TaskCompleteView(View, SingleObjectMixin):
    model = models.Task

    def post(self):
        task = self.get_object()
        task.toggle_complete()
        return HttpResponseRedirect(task.get_absolute_url())


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = TaskrUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return HttpResponseRedirect(reverse_lazy('taskr:index'))
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        redirect = super(RegisterView, self).form_valid(form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        if user is not None:
            auth_login(self.request, user)
        return redirect



class LoginView(FormView):
    template_name = 'login.html'
    form_class = TaskrUserLoginForm
    success_url = reverse_lazy('taskr:home')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user is not None:
            auth_login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        return self.form_invalid()

class LogoutView(RedirectView):
    url = reverse_lazy('taskr:index')

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).post(request, *args, **kwargs)
