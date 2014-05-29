from django.conf.urls import patterns, include, url
from taskr import urls as taskr_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^taskr/', include(taskr_urls, namespace='taskr')),
)
