from django.conf.urls import url
from test_sync.views import pushQueueView
from test_sync.views import viewQueueView

urlpatterns = [
    url(r'^push_queue/$', pushQueueView.as_view(), name='push_queue'),
    url(r'^view_queue/$', viewQueueView.as_view(), name='view_queue'),
]