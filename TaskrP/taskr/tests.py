from django.test import TestCase
from django.utils import timezone
from taskr.models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        now = timezone.now()
        Task.objects.create(id=1010, author_id=1, title='lots of time', deadline=(now+timezone.timedelta(days=30)))
        Task.objects.create(id=1011, author_id=1, title='just a day', deadline=(now+timezone.timedelta(hours=23)))
        Task.objects.create(id=1012, author_id=1, title='past deadline', deadline=(now-timezone.timedelta(days=3)))

    def test_task_deadlines(self):
        lots_of_time = Task.objects.get(pk=1010)

        self.assertEqual(lots_of_time.is_near_deadline(), False)
        self.assertEqual(lots_of_time.is_past_deadline(), False)

        just_a_day = Task.objects.get(pk=1011)

        self.assertEqual(just_a_day.is_near_deadline(), True)
        self.assertEqual(just_a_day.is_past_deadline(), False)

        past_deadline = Task.objects.get(pk=1012)

        self.assertEqual(past_deadline.is_near_deadline(), False)
        self.assertEqual(past_deadline.is_past_deadline(), True)