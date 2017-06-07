from django.conf.urls import url
from d3js_graph_movie_rating.views import IndexView
from d3js_graph_movie_rating.views import DataUpView
from d3js_graph_movie_rating.views import CorrMenWomenView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^data_up$', DataUpView.as_view(), name='data_up'),
    url(r'^corr_men_women$', CorrMenWomenView.as_view(), name='corr_men_women'),
]