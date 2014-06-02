from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return u'%s' % (self.user)

class Tag(models.Model):
    name = models.CharField(max_length=30)
    owner = models.OneToOneField(Author)

    def __str__(self):
        return u'%s' % (self.name)

# class Group(models.Model):
#     name = models.CharField(max_length=30)
#     owner = models.OneToOneField(Author)
#     members = models.ManyToManyField(Author, related_name='members')
#
#     def __str__(self):
#         return u'{%s} %s' % (self.id, self.name)

class Task(models.Model):
    author = models.ForeignKey(Author, unique=False)
    name = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, editable=False)
    edit_date = models.DateTimeField(auto_now_add=True, auto_now=True, editable=False)
    tag = models.ManyToManyField(Tag, related_name='tags', null=True, blank=True, default=None)
    # group = models.ForeignKey(Group, blank=True, default=None)

    def __str__(self):
        return u'%s' % (self.name)

    def toggle_complete(self):
        self.completed = not self.completed

    def is_past_deadline(self):
        return timezone.now() > self.deadline

    def get_absolute_url(self):
        return '/'