from django.conf.urls import url
from rating.views import DataUploadView, ScatterPlotView



urlpatterns = [
    url(r'^$', DataUploadView.as_view(), name='list'),  # as_view()はクラスベースで作った場合は定義しないといけない
    url(r'^scatterplot/', ScatterPlotView.as_view()),
]