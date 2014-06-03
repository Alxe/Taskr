from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from taskr import urls as taskr_urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^taskr/', include(taskr_urls, namespace='taskr')),
)
