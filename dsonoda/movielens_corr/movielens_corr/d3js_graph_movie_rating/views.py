from django.views import View
from django.shortcuts import render
from d3js_graph_movie_rating import models
from d3js_graph_movie_rating import forms
from d3js_graph_movie_rating import tasks
from d3js_graph_movie_rating import utils
from d3js_graph_movie_rating import consts
from django.http import HttpResponse
from hashlib import md5
import csv
import time
import json
# import pandas as pd
# from io import BytesIO
# from django.db import transaction
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

        # 並列処理ステータス
        sync_status = utils.get_sync_status_by_mode(consts.SYNC_MODE[0][0])

        # ファイルアップロードステータス
        movie_up_status = utils.get_fileupload_status(models.Movie)
        rating_up_status = utils.get_fileupload_status(models.Rating)
        user_info_up_status = utils.get_fileupload_status(models.UserInfo)

        form = forms.DataUpForm()
        return render(request, 'd3js_graph_movie_rating/data_up.html', {
            'form': form,
            'sync_status': sync_status,
            'movie_up_status': movie_up_status,
            'rating_up_status': rating_up_status,
            'user_info_up_status': user_info_up_status,
            'consts_sync_status': consts.SYNC_STATUS,
            'consts_fileupload_status': consts.FILEUPLOAD_STATUS
        })

    def post(self, request):
        """
        処理画面
        :param request:
        :return:
        """
        # taskid 生成
        queue_id = utils.get_queue_id()

        # ステータス登録 1: Celery にタスクを投げる
        if models.SyncStatus.objects.create(queue_id=queue_id, mode=consts.SYNC_MODE[0][0], status=consts.SYNC_STATUS[0][0]).id:
            movie_file = request.FILES["movie_file"].read()
            rating_file = request.FILES["rating_file"].read()
            user_file = request.FILES["user_file"].read()
            # Celery にキューを投げる
            # 並列に実行
            # apply_async() 、つまりCeleryにタスクが投げられる
            r = tasks.fileupload.apply_async(
                (json.dumps({
                    'movie': movie_file.decode('ISO-8859-1'),
                    'user_info': user_file.decode('ISO-8859-1'),
                    'rating': rating_file.decode('ISO-8859-1')
                }),
                queue_id)
            )
        else:
            raise Exception(111)

        return render(request, 'd3js_graph_movie_rating/data_up_end.html')


# グラフ表示のみ
class CorrMenWomenView(View):
    def get(self, request):
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

        # カラム名のバインド
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
