from django.conf.urls import url
from events.views import EventListView, EventDetailView, EventBookingList


urlpatterns = [
   url(r'^$', EventListView.as_view(), name='list'),
   url(r'(?P<event_id>[0-9]+)/$', EventDetailView.as_view(), name='detail'),
   url(r'^event_booking/$', EventBookingList.as_view(), name='event_booking'),
]