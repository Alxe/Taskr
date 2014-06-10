__author__ = 'Alex'

from ._mixin import FilterMultipleObjectMixin, UserFilterMultipleObjectMixin
from ._task import TaskListCreateView, TaskListActiveView, TaskListArchivedView, TaskDetailCompleteView

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

