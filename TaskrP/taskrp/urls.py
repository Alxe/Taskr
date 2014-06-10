from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from taskr_rest import urls as taskr_rest_urls
from taskr import urls as taskr_urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(taskr_rest_urls)),
    url(r'^', include(taskr_urls, namespace='taskr')),
)
