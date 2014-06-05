from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from taskr.views import IndexView, HomeView, TaskListView, TaskArchiveView, TaskDetailView, TaskCompleteView
from accounts.views import LoginView, LogoutView, RegisterView

urlpatterns = patterns('',
       url(r'^auth/login/$', LoginView.as_view(template_name='auth/login.html'), name='auth-login'),
       url(r'^auth/logout/$', LogoutView.as_view(), name='auth-logout'),
       url(r'^auth/register/$', RegisterView.as_view(template_name='auth/register.html'), name='auth-register'),

       url(r'^task/list/$', TaskListView.as_view(), name='task-list'),
       url(r'^task/archive/$', TaskArchiveView.as_view(), name='task-archive'),
       url(r'^task/(?P<pk>[1-9][0-9]*)/$', TaskDetailView.as_view(), name='task-detail'),
       url(r'^task/(?P<pk>[1-9][0-9]*)/complete/$', TaskCompleteView.as_view(), name='task-complete'),

       url(r'^users/(?P<pk>[1-9][0-9]*)/', IndexView.as_view(), name='user-profile'),

       url(r'^home/$', HomeView.as_view(), name='home'),
       url(r'^$', IndexView.as_view(), name='index'),
)
