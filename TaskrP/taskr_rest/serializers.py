from rest_framework import serializers
from taskr.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'completed', 'pub_date', 'deadline')