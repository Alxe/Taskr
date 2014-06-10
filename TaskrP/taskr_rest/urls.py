from django.conf.urls import patterns, url, include
from rest_framework import routers
from .views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'task', TaskViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)