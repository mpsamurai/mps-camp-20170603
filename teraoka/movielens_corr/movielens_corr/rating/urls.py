from django.conf.urls import url
from rating.views import DataUploadView
from rating.views import DataUploadView, ReadToCsv, ScatterPlotView


urlpatterns = [
    url(r'^$', DataUploadView.as_view(), name='list'),
    url(r'^readtocsv/', ReadToCsv.as_view(), name='readtocsv'),
    url(r'^scatterplotview/', ScatterPlotView.as_view(), name='scatterplotview'),
]