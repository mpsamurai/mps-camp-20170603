from django.conf.urls import url
from events.views import EventListView
from events.views import EventDetailView

urlpatterns = [
   url(r'^$', EventListView.as_view(), name='event-list'),
   url(r'(?P<event_id>[0-9]+)/$', EventDetailView.as_view(), name='event_id'),
]