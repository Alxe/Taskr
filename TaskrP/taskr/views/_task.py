from django.utils.decorators import method_decorator

__author__ = 'Alex'

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, CreateView
from ._mixin import UserFilterMultipleObjectMixin
from ..models import Task
from ..forms import TaskCreateForm, TaskCompleteForm


class TaskListCreateView(UserFilterMultipleObjectMixin, CreateView):
    form_class = TaskCreateForm
    queryset = Task.objects.filter(completed=False)
    template_name = 'home.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('taskr:home')
    attr = 'author_id'
    offset = None
    limit = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskListCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        return super(TaskListCreateView, self).form_valid(form)


class TaskListActiveView(UserFilterMultipleObjectMixin, TemplateView):
    queryset = Task.objects.filter(completed=False)
    template_name = 'task/list.html'
    context_object_name = 'tasks'
    attr = 'author_id'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskListActiveView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset


class TaskListArchivedView(TaskListActiveView):
    queryset = Task.objects.filter(completed=True)
    template_name = 'task/archive.html'


class TaskDetailCompleteView(FormMixin, DetailView):
    form_class = TaskCompleteForm
    template_name = 'task/detail.html'
    model = Task
    context_object_name = 'task'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy('taskr:task-detail', kwargs={'pk': kwargs['pk']})
        return super(TaskDetailCompleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return super(TaskDetailCompleteView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        task = Task.objects.get(pk=form.cleaned_data['id'])
        task.toggle_complete(commit=False)
        task.save()
        return super(TaskDetailCompleteView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TaskDetailCompleteView, self).get_context_data(**kwargs)
        form = self.get_form(self.form_class)
        if form:
            context['form'] = form
        context.update(kwargs)
        return super(TaskDetailCompleteView, self).get_context_data(**context)
