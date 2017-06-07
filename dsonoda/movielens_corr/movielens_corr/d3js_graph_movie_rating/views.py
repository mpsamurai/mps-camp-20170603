from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'd3js_graph_movie_rating/index.html', {})

class DataUpView(View):
    def get(self, request):
        return render(request, 'd3js_graph_movie_rating/data_up.html', {})

class CorrMenWomenView(View):
    def get(self, request):
        return render(request, 'd3js_graph_movie_rating/corr_men_women.html', {})
