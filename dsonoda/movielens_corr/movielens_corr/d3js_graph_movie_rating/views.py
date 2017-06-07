from django.shortcuts import render

# Create your views here.
from django.views import View
from d3js_graph_movie_rating import forms
import csv
import pandas as pd
from io import BytesIO
from d3js_graph_movie_rating import models


class IndexView(View):
    def get(self, request):
        return render(request, 'd3js_graph_movie_rating/index.html', {})

class DataUpView(View):
    def get(self, request):
        form = forms.DataUpForm()
        return render(request, 'd3js_graph_movie_rating/data_up.html', {'form': form})

    def post(self, request):
        # ファイルを受け取り
        movie_data = pd.read_csv(BytesIO(request.FILES["movie_file"].read()),
                    sep='::', header=None,
                    names=['mid', 'title', 'genres'], encoding='ISO-8859-1')
        rating_data = pd.read_csv(BytesIO(request.FILES["rating_file"].read()),
                    sep='::', header=None,
                    names=['uid', 'mid', 'rating', 'timestamp'], encoding='ISO-8859-1')
        user_data = pd.read_csv(BytesIO(request.FILES["user_file"].read()),
                    sep='::', header=None,
                    names=['uid', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')

        # DB格納
        for i, (mid, title, genres) in movie_data.iterrows():
            obj = models.Movie.objects.create(mid=mid, title=title)

        # レーティング情報は多すぎるため任意の件数でカット
        cnt = 0
        for i, (uid, mid, rating, timestamp) in rating_data.iterrows():
            obj = models.Rating.objects.create(uid=uid, mid=mid, rating=rating)
            if cnt > 6000:
                break
            cnt += 1

        for i, (uid, gender, age, occupation, zip_code) in user_data.iterrows():
            obj = models.UserInfo.objects.create(uid=uid, gender=gender)

        return self.get(request)

class CorrMenWomenView(View):
    def get(self, request):
        return render(request, 'd3js_graph_movie_rating/corr_men_women.html', {})
