from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
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
            return HttpResponseRedirect(reverse('taskr:home'))
        return super(IndexView, self).dispatch(request, *args, **kwargs)

class HomeView(CreateView, MultipleObjectMixin):
    # common
    model = models.Task
    template_name = 'home.html'

    #form
    fields = ['title', 'description', 'tag', 'completed', 'deadline', 'author']
    initial = {'completed' : True, 'deadline' : None, 'author' : models.Author.objects.get(pk=1)}

    # list
    object_list = model.objects.all()
    context_object_name = 'tasks'
    paginate_by = 40


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('taskr:index'))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.initial['author_id'] = get_object_or_404(models.Author, pk=request.user.id)
        return super(HomeView, self).post(request, *args, **kwargs)

class TaskDetailView(DetailView):
    model = models.Task
    template_name = 'task_detail.html'