from django.conf.urls import patterns, url
from django.views.generic import ListView
from todo_app.models import Item

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Item.objects.order_by('priority')[:5],
            context_object_name='latest_todo_list',
            template_name='todo/index.html'
        )),
    # url(r'^todo/', include('todo_app/urls')),
    # url(r'^todo/', include('todo_app/urls')),
    # url(r'^todo/', include('todo_app/urls')),
    # url(r'^todo/', include('todo_app/urls')),
)
