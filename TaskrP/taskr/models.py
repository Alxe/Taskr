from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class TaskrUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True,
                      is_staff=is_staff, is_superuser=is_superuser,
                      last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user( email, password, True, True, **extra_fields)


class TaskrUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = TaskrUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_absolute_url(self):
        return reverse('taskr:user-profile', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return u'%s' % (self.user)

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
    deadline = models.DateTimeField(null=True, blank=True)
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
        return (self.deadline - timezone.timedelta(days=days)) > timezone.now()

    def is_past_deadline(self):
        return (timezone.now() > self.deadline) if self.deadline else False

    def get_absolute_url(self):
        return reverse('taskr:task-detail', kwargs={'pk': self.id })