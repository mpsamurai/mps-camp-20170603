from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from rating.form import UploadFileForm
from django.views import View
from rating.form import UploadFileForm
from rating.models import Movie, UserProfile, Rating
import pandas as pd
from io import BytesIO, StringIO  # BytesIOはバイトファイルを返還処理する組込みメソッド
from django.db.models import Avg
from django.http import HttpResponse


class DataUploadView(View):
    """
    Postされてきたrequestをdata加工してDBへ保存
    return: None
    """
    def get(self, request):
        return render(request, 'rating/data_upload.html', {})

    def post(self, request):

        # movies = Movie()
        # movie_df = pd.read_csv(BytesIO(request.FILES["movie-file"].read()),
        #                      sep='::', header=None,
        #                      names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')
        # for _, (mid, title, _) in movie_df.iterrows():  # pandasの行を一度にとってくる
        #     movies = Movie(mid=mid, title=title)     # 使わないものは _ にする
        #     movies.save()
        #
        # users = UserProfile()
        # user_df = pd.read_csv(BytesIO(request.FILES["user-file"].read()),
        #                      sep='::', header=None,
        #                      names=['user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')
        # for _, (user_id, gender, _, _, _) in user_df.iterrows():
        #     users = UserProfile(uid=user_id, gender=gender)
        #     users.save()
        #
        # ratings = Rating()
        # rating_df = pd.read_csv(BytesIO(request.FILES["rating-file"].read()),
        #                      sep='::', header=None,
        #                      names=['user_id', 'movie_id', 'rating', 'timestamp'], encoding='ISO-8859-1')
        # count = 0
        # for _, (uid, mid, rating, _) in rating_df.iterrows():
        #     count += 1
        #     if count < 3000:
        #         user_profile = UserProfile.objects.get(uid=uid)  # UserProfileクラスのuidをとってくる
        #         movie = Movie.objects.get(mid=mid)  # Movieクラスのmidをとってくる
        #         ratings = Rating.objects.create(user_profile=user_profile, movie=movie, score=rating)  # 上でとっているidをRatingクラスに入れる(紐付ける)
        #         ratings.save()
        #     else:
        #         break

        return render(request, 'rating/upload_complete.html', {})




        # return render(request, 'rating/upload_complete.html',
        #               {"movies_title": movies.title,
        #                "users_title": users.gender,
        #                "ratings_title": ratings.rating})

class ReadToCsv(View):
    """
    DBよりgetしたdataからある映画に対しての男女別のRating平均値をだす
    return: 映画タイトル・男性平均score・女性平均score
    """
    def get(self, request):

        movies = Movie.objects.all()
        movies_ratings = {'movie': [], 'male_average': [], 'female_average': []}
        for movie in movies:

            ratings = Rating.objects.filter(movie__mid=movie.mid)
            male_ratings = ratings.filter(user_profile__gender='M')

            female_ratings = ratings.filter(user_profile__gender='F')
            male_average = male_ratings.aggregate(Avg('score'))
            female_average = female_ratings.aggregate(Avg('score'))

            movies_ratings['movie'].append(movie)
            movies_ratings['male_average'].append(male_average["score__avg"])
            movies_ratings['female_average'].append(female_average["score__avg"])
            #raise Exception(movies_ratings)
        movie_ratings_df = pd.DataFrame.from_dict(movies_ratings)
        movie_ratings_df = movie_ratings_df.fillna(0)


        raise Exception("OK", movie_ratings_df)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename ="rating.csv"'
        movie_ratings_df.to_csv(response, index=False)
        # raise Exception(response)
        return response


class ScatterPlotView(View):

    def get(self, request):
        get_rating_csv = ReadToCsv()
        return render(request, 'rating/scatterplotview.html', {'get_rating_csv': get_rating_csv})
