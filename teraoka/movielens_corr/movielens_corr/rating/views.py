from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from rating.form import UploadFileForm
from django.views import View
from rating.form import UploadFileForm
from rating.models import Movie
import pandas as pd
from io import BytesIO, StringIO

"""
BytesIOがfile
"""

class DataUploadView(View):

    def get(self, request):
        return render(request, 'rating/data_upload.html', {})

    def post(self, request):
        movies = pd.read_csv(BytesIO(request.FILES["movie-file"].read()),
                             sep='::', header=None,
                             names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')

        users = pd.read_csv(BytesIO(request.FILES["user-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')

        ratings = pd.read_csv(BytesIO(request.FILES["rating-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'movie_id', 'rating', 'timestamp'], encoding='ISO-8859-1')


        #raise Exception(movies.title)




        return render(request, 'rating/upload_complete.html',
                      {"movies_title": movies.title,
                       "users_title": users.gender,
                       "ratings_title": ratings.rating})
