from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^todo/', include('todo_app/urls')),
    url(r'^admin/', include(admin.site.urls)),
)
