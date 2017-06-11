from django.conf.urls import url
from rating.views import DataUploadView
from rating.views import DataUploadView, ReadToCsv, ScatterPlotView, UploadEnd, ErrorView, GetProgress

urlpatterns = [
    url(r'^$', DataUploadView.as_view(), name='list'),
    url(r'^readtocsv/', ReadToCsv.as_view(), name='readtocsv'),
    url(r'^scatterplotview/', ScatterPlotView.as_view(), name='scatterplotview'),
    url(r'^uploadend/$', UploadEnd.as_view(), name='uploadend'),
    url(r'^eoferror/$', ErrorView.as_view(), name='eoferror'),
    url(r'^getprogress/$', GetProgress.as_view(), name='getprogress'),
    # クラスを呼び出したいだけでもこのnameを呼べばいい(その際、テンプレートは必要ない：getprogressの時)
]