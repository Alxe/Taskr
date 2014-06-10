from django.conf.urls import url
from accounts.views import LoginView, LogoutView, RegisterView
from django.contrib.auth.decorators import login_required
from .views import IndexView, TaskListCreateView, TaskListActiveView, TaskListArchivedView, TaskDetailCompleteView

urlpatterns = [
    url(r'^auth/login/$', LoginView.as_view(template_name='auth/login.html'), name='auth-login'),
    url(r'^auth/logout/$', LogoutView.as_view(), name='auth-logout'),
    url(r'^auth/register/$', RegisterView.as_view(template_name='auth/register.html'), name='auth-register'),

    # url(r'^profile/$', ProfileView.as_view(), name='author-profile-self' ),
    # url(r'^profile/(?P<pk>[1-9][0-9]*)/$', ProfileView.as_view(), name='author-profile'),

    url(r'^task/list/$', TaskListActiveView.as_view(), name='task-list'),
    url(r'^task/archive/$', TaskListArchivedView.as_view(), name='task-archive'),
    url(r'^task/(?P<pk>[1-9][0-9]*)/$', TaskDetailCompleteView.as_view(), name='task-detail'),

    url(r'^users/(?P<pk>[1-9][0-9]*)/', IndexView.as_view(), name='user-profile'),

    url(r'^task/$', TaskListCreateView.as_view(), name='home'),
    url(r'^$', IndexView.as_view(), name='index'),
]
