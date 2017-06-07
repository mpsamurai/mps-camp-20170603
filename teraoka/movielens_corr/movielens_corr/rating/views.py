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
        title = Movie()
        movies = pd.read_csv(BytesIO(request.FILES["movie-file"].read()),
                             sep='::', header=None,
                             names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')
        for titles in movies['title']:
            movie = Movie(title=titles)
            movie.save()

        user = User()
        users = pd.read_csv(BytesIO(request.FILES["user-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')
        for user_id, gender in zip(users['user_id'],users['gender']):
            user = User(user=user_id, gender=gender)
            user.save()

        rating = Rating()
        ratings = pd.read_csv(BytesIO(request.FILES["rating-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'movie_id', 'rating', 'timestamp'], encoding='ISO-8859-1')
        for rating in ratings['rating']:
            rating = Rating(score=rating)
            rating.save()


        raise Exception("test", movies['title'], user['gender'])




        return render(request, 'rating/upload_complete.html',
                      {"movies_title": movies.title,
                       "users_title": users.gender,
                       "ratings_title": ratings.rating})
