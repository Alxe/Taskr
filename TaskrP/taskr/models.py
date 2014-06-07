from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AuthorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return u'%s' % self.user

    def get_absolute_url(self):
        return reverse('taskr:user-profile', kwargs={'pk': self.user.id})


# class Tag(models.Model):
#     name = models.CharField(max_length=30)
#     owner = models.OneToOneField(settings.AUTH_USER_MODEL)


# class Group(models.Model):
#     name = models.CharField(max_length=30)
#     owner = models.OneToOneField(settings.AUTH_USER_MODEL)
#     members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False)
    title = models.CharField(max_length=255)
    # content = models.TextField(blank=True, max_length=255, default='')
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True, default=None)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    edit_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)
    # tag = models.ManyToManyField(Tag, related_name='tags', null=True, blank=True, default=None)
    # group = models.ForeignKey(Group, blank=True, default=None)

    absolute_url = None

    def __str__(self):
        return u'%s' % (self.title)

    def toggle_complete(self, commit=True):
        self.completed = not self.completed

        if commit:
            self.save()

    def is_near_deadline(self, days=1):
        if self.is_past_deadline():
            return False
        return (self.deadline-timezone.timedelta(days=days)) < timezone.now()

    def is_past_deadline(self):
        return (self.deadline < timezone.now()) if self.deadline else False

    def get_absolute_url(self):
        return reverse('taskr:task-detail', kwargs={'pk': self.id })