from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
# from rating.form import UploadFileForm
from django.views import View
from rating.form import UploadFileForm
from rating.models import Movie, UserProfile, Rating, DataUploadTask
import pandas as pd
from io import BytesIO, StringIO  # BytesIOはバイトファイルを返還処理する組込みメソッド
from django.db.models import Avg
from django.http import HttpResponse
from django.db import transaction
import csv
from rating import tasks
from celery.utils.log import get_task_logger


class DataUploadView(View):
    """
    Postされてきたrequestをdata加工してDBへ保存
    return: None
    """
    def get(self, request):
        return render(request, 'rating/data_upload.html', {})

    def post(self, request):
        try:
            movie_file = request.FILES["movie-file"].read()
            user_file = request.FILES["user-file"].read()
            rating_file = request.FILES["rating-file"].read()
            import json
            # celeryがtidを生成している
            #tasks = DataUploadTask.objects.all()  # modelsのインスタンスを全て取ってくる
            # raise Exception(task.complete)
            if DataUploadTask.objects.filter(complete=False).exists():
                message = '前の計算が終わっていないのでしばらく少し待ってから問い合わせてください'
                return render(request, 'rating/eoferror.html', {'message': message})
            else:
                r = tasks.data_upload.delay(json.dumps({'m': movie_file.decode('ISO-8859-1'),
                                                        'u': user_file.decode('ISO-8859-1'),
                                                        'r': rating_file.decode('ISO-8859-1')}))
                task = DataUploadTask.objects.create(state='キューが投げられました', tid=r.task_id)
                task.save()
                return redirect('rating:uploadend')
        except KeyError:
            message = 'ファイルが選択されていません'
            return render(request, 'rating/eoferror.html', {'message': message})

        except NameError:
            message = 'ファイルが選択されていません'
            return render(request, 'rating/eoferror.html', {'message': message})

        # finally:  # try後でも何が行われてもここは実行する
        #     return redirect('rating:eoferror')


class ErrorView(View):
    def get(self, request):
        return render(request, 'rating/eoferror.html' )


class UploadEnd(View):
    def get(self, request):
        task = DataUploadTask.objects.all()
        task
        # raise Exception(taskTables)
        return render(request, 'rating/data_uploadend.html', {'task': task})

class GetProgress(View):
    def get(self, request):  # 以下で取得することで唯一のもののインスタンスがとれるのでこれが使える
        try:
            tasks = DataUploadTask.objects.get(complete=False)  # 唯一のものを抜き出す方法が[False,False,False,True] 現在進行のものがTrueである
            progress_list = []
            progress_list.append(tasks.progress)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment;filename ="rating.csv"'
            writer = csv.writer(response)
            writer.writerow(['progress'])
            writer.writerow(progress_list)
            return response
        except DataUploadTask.DoesNotExist:
            pass
            message = 'データ転送が完了しました'
            return render(request, 'rating/scatterplotview.html', {'message': message})


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
        movie_ratings_df = pd.DataFrame.from_dict(movies_ratings)
        movie_ratings_df = movie_ratings_df.fillna(0)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename ="rating.csv"'
        movie_ratings_df.to_csv(response, index=False)
        # raise Exception(response)
        return response


class ScatterPlotView(View):

    def get(self, request):
        get_rating_csv = ReadToCsv()
        return render(request, 'rating/scatterplotview.html', {'get_rating_csv': get_rating_csv})





