from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from taskr.views import IndexView, HomeView, TaskListView, TaskArchiveView, TaskDetailView, TaskCompleteView, RegisterView, LoginView, LogoutView

urlpatterns = patterns('',
       url(r'^auth/login/$', LoginView.as_view(), name='auth-login'),
       url(r'^auth/logout/$', LogoutView.as_view(), name='auth-logout'),
       url(r'^auth/register/$', RegisterView.as_view(), name='auth-register'),

       url(r'^task/(?P<pk>[1-9][0-9]*)/complete/$', TaskCompleteView.as_view(), name='task-detail'),
       url(r'^task/(?P<pk>[1-9][0-9]*)/$', TaskDetailView.as_view(), name='task-detail'),
       url(r'^task/archive/$', TaskArchiveView.as_view(), name='task-archive'),
       url(r'^task/$', TaskListView.as_view(), name='task-list'),

       url(r'^users/?P<pk>[1-9][0-9]*/', IndexView.as_view(), name='user-profile'),

       url(r'^home/$', HomeView.as_view(), name='home'),
       url(r'^$', IndexView.as_view(), name='index'),
)
