from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import MultipleObjectMixin
from taskr import models
from taskr.forms import TaskForm

class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('taskr:home'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class HomeView(CreateView, MultipleObjectMixin):
    # common
    model = models.Task
    template_name = 'home.html'

    #form
    form_class = TaskForm

    # list
    object_list = model.objects.all()
    context_object_name = 'tasks'
    paginate_by = 40

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('taskr:index'))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = models.Author.objects.get(user=self.request.user)  # use your own profile here
        task.save()
        return HttpResponseRedirect(self.success_url if self.success_url is not None else task.get_absolute_url())

class TaskDetailView(DetailView):
    model = models.Task
    template_name = 'task_detail.html'