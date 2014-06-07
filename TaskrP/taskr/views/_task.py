from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormMixin
from ..forms import TaskCreateForm
from taskr.forms import TaskCompleteForm

__author__ = 'Alex'

from django.views.generic import TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin, DetailView
from ._mixin import UserFilterMultipleObjectMixin
from ..models import Task


class TaskListView(UserFilterMultipleObjectMixin, TemplateView):
    queryset = Task.objects.filter(completed=False)
    template_name = 'task/list.html'
    context_object_name = 'tasks'
    attr = 'author_id'

    def get_queryset(self):
        return self.queryset


class TaskArchiveView(TaskListView):
    queryset = Task.objects.filter(completed=True)


class TaskDetailView(FormMixin, DetailView):
    form_class = TaskCompleteForm
    template_name = 'task/detail.html'
    model = Task
    context_object_name = 'task'

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy('taskr:task-detail', kwargs={'pk': kwargs['pk']})
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            return self.form_valid(form)
        return super(TaskDetailView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        task = Task.objects.get(pk=form.cleaned_data['id'])
        task.toggle_complete(commit=False)
        task.save()
        return super(TaskDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        form = self.get_form(self.form_class)
        if form:
            context['form'] = form
        context.update(kwargs)
        return super(TaskDetailView, self).get_context_data(**context)
