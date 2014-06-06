__author__ = 'Alex'

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.detail import SingleObjectMixin
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


class TaskDetailView(DetailView):
    template_name = 'task/detail.html'
    queryset = Task.objects.all()


class TaskCompleteView(View, SingleObjectMixin):
    model = Task

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.toggle_complete()
        return HttpResponseRedirect(task.get_absolute_url())