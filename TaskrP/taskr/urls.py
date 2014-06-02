from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from taskr.views import IndexView, HomeView, TaskDetailView, RegisterView

namespace = 'taskr'

urlpatterns = patterns('',
    url(r'^auth/login/$', 'django.contrib.auth.views.login', {'template_name' : 'login.html', 'redirect_field_name' : 'next'}, name='auth-login'),
    url(r'^auth/logout/$', 'django.contrib.auth.views.logout', {'next_page' : reverse_lazy('taskr:index')}, name='auth-logout'),
    url(r'^auth/register/$', RegisterView.as_view(), name='auth-register'),
    url(r'^task/(?P<pk>[1-9][0-9]*)/$', TaskDetailView.as_view(), name='task-detail'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^$', IndexView.as_view(), name='index'),
)
