from django.conf.urls import patterns, include, url

from django.contrib import admin
from ligoapp.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main_page),
    url(r'^admin/', include(admin.site.urls)),
)
