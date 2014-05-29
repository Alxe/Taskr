from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import MultipleObjectMixin
from taskr import models

class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('')
        return super(IndexView, self).dispatch(self, request, *args, **kwargs)

class HomeView(CreateView, MultipleObjectMixin):
    model = models.Task
    template_name = 'home.html'
    object_list = model.objects.all()
    context_object_name = 'tasks'
    paginate_by = 40


class TaskDetailView(DetailView):
    model = models.Task
    template_name = 'task_detail.html'