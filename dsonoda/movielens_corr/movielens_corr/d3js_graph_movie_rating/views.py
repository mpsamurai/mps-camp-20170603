from django.views import View
from django.shortcuts import render
from d3js_graph_movie_rating import models
from d3js_graph_movie_rating import forms
from d3js_graph_movie_rating import tasks
import csv
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Avg


class IndexView(View):
    def get(self, request):
        return render(request, 'd3js_graph_movie_rating/index.html', {})

class DataUpView(View):
    def get(self, request):
        """
        入力画面
        :param request:
        :return:
        """
        form = forms.DataUpForm()
        return render(request, 'd3js_graph_movie_rating/data_up.html', {'form': form})

    def post(self, request):
        """
        処理画面
        :param request:
        :return:
        """
        # ファイルを受け取り
        movie_data = pd.read_csv(BytesIO(request.FILES["movie_file"].read()),
            sep='::',
            header=None,
            names=['mid', 'title', 'genres'],
            encoding='ISO-8859-1')
        rating_data = pd.read_csv(BytesIO(request.FILES["rating_file"].read()),
            sep='::',
            header=None,
            names=['uid', 'mid', 'rating', 'timestamp'],
            encoding='ISO-8859-1')
        user_data = pd.read_csv(BytesIO(request.FILES["user_file"].read()),
            sep='::',
            header=None,
            names=['uid', 'gender', 'age', 'occupation', 'zip'],
            encoding='ISO-8859-1')

        with transaction.atomic():
            # DB格納
            for i, (mid, title, genres) in movie_data.iterrows():
                obj = models.Movie.objects.create(
                    mid = mid,
                    title = title)

            for i, (uid, gender, age, occupation, zip_code) in user_data.iterrows():
                obj = models.UserInfo.objects.create(
                    uid=uid,
                    gender=gender)

            # レーティング情報は多すぎるため任意の件数でカット
            cnt = 3000
            for i, (r_uid, r_mid, rating, timestamp) in rating_data.iterrows():
                movie = models.Movie.objects.get(mid=r_mid)
                user_info = models.UserInfo.objects.get(uid=r_uid)
                obj = models.Rating.objects.create(user_info=user_info, movie=movie, rating=rating)
                if cnt == 0:
                    break
                cnt -= 1

        return self.get(request)

    # def end(self, request):
    #     """
    #     完了画面
    #     :param request:
    #     :return:
    #     """
    #     return render(request, 'd3js_graph_movie_rating/data_up_end.html', {})


# グラフ表示のみ
class CorrMenWomenView(View):
    def get(self, request):
        # avg_ratings = []
        # for movie in models.Movie.objects.all():
        #     female_avg = models.Rating.objects.filter(movie=movie, user_info__gender="F").aggregate(Avg('rating'))
        #     male_ave = models.Rating.objects.filter(movie=movie, user_info__gender="M").aggregate(Avg('rating'))
        #     avg_ratings.append([movie.title, female_avg['rating__avg'], male_ave['rating__avg']])
        # raise Exception(avg_ratings)

        return render(request, 'd3js_graph_movie_rating/corr_men_women.html', {})


# データ生成、取得
class GetCorrMenWomenView(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        writer = csv.writer(response)

        # レーティング平均
        avg_ratings = []
        for movie in models.Movie.objects.all():
            # DBの相関を利用して平均データを取得
            female_avg = models.Rating.objects.filter(movie=movie, user_info__gender="F").aggregate(Avg('rating'))
            male_ave = models.Rating.objects.filter(movie=movie, user_info__gender="M").aggregate(Avg('rating'))
            # レーティングが None だったら 0 をセット
            if female_avg['rating__avg'] is None:
                female_avg['rating__avg'] = 0
            if male_ave['rating__avg'] is None:
                male_ave['rating__avg'] = 0
            avg_ratings.append([movie.title, female_avg['rating__avg'], male_ave['rating__avg']])
        # raise Exception(avg_ratings)
        writer.writerow(['title', 'female', 'male'])
        writer.writerows(avg_ratings)

        return response


class AddWithSleepSyncView(View):
    def get(self, request):
        # 直列に実行
        r = tasks.add_with_sleep.apply((2,3))
        return HttpResponse('The answer is %s' % r.get())

class AddWithSleepAsyncView(View):
    def get(self, request):
        # 並列に実行
        # delay の分待つことになったらCelery にタスクを投げる
        r = tasks.add_with_sleep.delay(2,3)
        return HttpResponse('The answer is queued %s' % r)
