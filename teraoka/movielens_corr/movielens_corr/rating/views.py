from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from rating.form import UploadFileForm
from django.views import View
from rating.form import UploadFileForm
from rating.models import Movie, UserProfile, Rating
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
        movie_df = pd.read_csv(BytesIO(request.FILES["movie-file"].read()),
                             sep='::', header=None,
                             names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')
        for _, (mid, title, _) in movie_df.iterrows():  # pandasの行を一度にとってくる
            movies = Movie(mid=mid, title=title)     # 使わないものは _ にする
            movies.save()

        users = UserProfile()
        user_df = pd.read_csv(BytesIO(request.FILES["user-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')
        for _, (user_id, gender, _, _, _) in user_df.iterrows():
            users = UserProfile(uid=user_id, gender=gender)
            users.save()

        ratings = Rating()
        rating_df = pd.read_csv(BytesIO(request.FILES["rating-file"].read()),
                             sep='::', header=None,
                             names=['user_id', 'movie_id', 'rating', 'timestamp'], encoding='ISO-8859-1')
        count = 0
        for _, (uid, mid, rating, _) in rating_df.iterrows():
            count += 1
            if count < 3000:
                user_profile = UserProfile.objects.get(uid=uid)  # UserProfileクラスのuidをとってくる
                movie = Movie.objects.get(mid=mid)  # Movieクラスのmidをとってくる
                ratings = Rating.objects.create(user_profile=user_profile, movie=movie, score=rating)  # 上でとっているidをRatingクラスに入れる(紐付ける)
                ratings.save()
            else:
                break

        # raise Exception("tt", rating_data)
        # raise Exception("test", movies['title'], users['gender'])




        return render(request, 'rating/upload_complete.html',
                      {"movies_title": movies.title,
                       "users_title": users.gender,
                       "ratings_title": ratings.rating})
