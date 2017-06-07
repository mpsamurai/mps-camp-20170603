from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from rating.form import UploadFileForm
from django.views import View
from rating.form import UploadFileForm
from rating.models import Movie, User, Rating
import pandas as pd
from io import BytesIO, StringIO

"""
BytesIOがfile
"""

class DataUploadView(View):

    def get(self, request):
        return render(request, 'rating/data_upload.html', {})

    def post(self, request):
        movies = Movie()
        movie_data = pd.read_csv(BytesIO(request.FILES["movie-file"].read()),
                             sep='::', header=None,
                             names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')
        for title in movie_data['title']:
            movies = Movie(title=title)
            movies.save()

        users = User()
        user_data = pd.read_csv(BytesIO(request.FILES["user-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')
        for user_id, gender in zip(user_data['user_id'], user_data['gender']):
            users = User(user=user_id, gender=gender)
            users.save()

        ratings = Rating()
        rating_data = pd.read_csv(BytesIO(request.FILES["rating-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'movie_id', 'rating', 'timestamp'], encoding='ISO-8859-1')
        for rating in rating_data['rating']:
            ratings = Rating(score=rating)
            ratings.save()

        # raise Exception("tt", rating_data)
        raise Exception("test", movies['title'], users['gender'])




        return render(request, 'rating/upload_complete.html',
                      {"movies_title": movies.title,
                       "users_title": users.gender,
                       "ratings_title": ratings.rating})
