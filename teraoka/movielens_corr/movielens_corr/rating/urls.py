from django.conf.urls import url
from rating.views import DataUploadView, Test



urlpatterns = [
    url(r'^$', DataUploadView.as_view(), name='list'),
    url(r'^test/', Test.as_view()),
]