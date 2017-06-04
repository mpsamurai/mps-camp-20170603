from django.conf.urls import url
from events.views import EventListView, EventDetailView


urlpatterns = [
   url(r'^$', EventListView.as_view(), name='list'),
   url(r'(?P<event_id>[0-9]+)/$', EventDetailView.as_view(), name='detail'),
]