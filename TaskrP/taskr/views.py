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
from .models import Task
from .forms import TaskCreateForm


class AuthorBasedMultipleTaskMixin(MultipleObjectMixin):
    offset = None
    limit = None

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(author_id=self.request.user.id)
        if (self.offset is not None) and (self.offset >= 0) and (self.offset < queryset.count()):
            queryset = queryset.filter()[self.offset:]
        if (self.limit is not None) and (self.limit >= 0) and (self.limit < queryset.count()):
            queryset = queryset.filter()[:self.limit]
        context_object_name = self.get_context_object_name(queryset)
        context = {
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            'object_list': queryset
        }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super(MultipleObjectMixin, self).get_context_data(**context)


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('taskr:home'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class HomeView(CreateView, AuthorBasedMultipleTaskMixin):
    form_class = TaskCreateForm
    queryset = Task.objects.filter(completed=False)
    template_name = 'home.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('taskr:home')
    offset = None
    limit = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('taskr:index'))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        return super(HomeView, self).form_valid(form)


class TaskListView(ListView, AuthorBasedMultipleTaskMixin):
    queryset = Task.objects.filter(completed=False)
    template_name = 'task/list.html'
    context_object_name = 'tasks'


class TaskArchiveView(TaskListView):
    queryset = Task.objects.filter(completed=True)
    template_name = 'task/archive.html'


class TaskDetailView(DetailView):
    template_name = 'task/detail.html'
    queryset = Task.objects.all()


class TaskCompleteView(View, SingleObjectMixin):
    model = Task

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.toggle_complete()
        return HttpResponseRedirect(task.get_absolute_url())