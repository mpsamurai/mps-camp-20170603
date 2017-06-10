from django.conf.urls import url
from d3js_graph_movie_rating.views import IndexView
from d3js_graph_movie_rating.views import DataUpView
from d3js_graph_movie_rating.views import CorrMenWomenView
from d3js_graph_movie_rating.views import GetCorrMenWomenView
from d3js_graph_movie_rating.views import AddWithSleepSyncView
from d3js_graph_movie_rating.views import AddWithSleepAsyncView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^data_up/$', DataUpView.as_view(), name='data_up'),
    url(r'^corr_men_women/$', CorrMenWomenView.as_view(), name='corr_men_women'),
    url(r'^get_corr_men_women/$', GetCorrMenWomenView.as_view(), name='get_corr_men_women'),
    url(r'^add_with_sleep_sync/$', AddWithSleepSyncView.as_view(), name='add_with_sleep_sync'),
    url(r'^add_with_sleep_a_sync/$', AddWithSleepAsyncView.as_view(), name='add_with_sleep_a_sync'),
]