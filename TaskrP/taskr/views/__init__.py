__author__ = 'Alex'

from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from ._mixin import FilterMultipleObjectMixin, UserFilterMultipleObjectMixin
from ._task import TaskListView, TaskArchiveView, TaskDetailView, TaskCompleteView
from ..forms import TaskCreateForm
from ..models import Task


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('taskr:home'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class HomeView(UserFilterMultipleObjectMixin, CreateView):
    form_class = TaskCreateForm
    queryset = Task.objects.filter(completed=False)
    template_name = 'home.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('taskr:home')
    attr = 'author_id'
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


