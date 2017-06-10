from movielens_corr.celery import app as celery_app
from celery.utils.log import get_task_logger
from rating.models import Movie, UserProfile, Rating, DataUploadTask
import pandas as pd
from io import BytesIO, StringIO
from django.db import transaction
import json

logger = get_task_logger(__name__)

@celery_app.task(bind=True)
def data_upload(self, files):
    files = json.loads(files)
    movies = Movie()
    movie_df = pd.read_csv(StringIO(files['m']),
                           sep='::', header=None,
                           names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')
    #print(movie_df)
    with transaction.atomic():
        for _, (mid, title, _) in movie_df.iterrows():  # pandasの行を一度にとってくる
            movies = Movie(mid=mid, title=title)  # 使わないものは _ にする
            movies.save()

    users = UserProfile()
    user_df = pd.read_csv(StringIO(files['u']),
                          sep='::', header=None,
                          names=['user_id', 'gender', 'age', 'occupation', 'zip'], encoding='ISO-8859-1')
    with transaction.atomic():
        for _, (user_id, gender, _, _, _) in user_df.iterrows():
            users = UserProfile(uid=user_id, gender=gender)
            users.save()


    ratings = Rating()
    rating_df = pd.read_csv(StringIO(files['r']),
                            sep='::', header=None,
                            names=['user_id', 'movie_id', 'rating', 'timestamp'], encoding='ISO-8859-1')
    #ファイルの個数を調べる
    rating_length = len(rating_df)
    # logger.info("最初 %s" % rating_length)
    rating_df_grouped = (rating_df.groupby('movie_id').size())

    rating_df_grouped = rating_df_grouped.sort_values(ascending=False)
    rating_df_grouped = rating_df_grouped.head(20)

    # raise Exception(rating_df)
    rating_df = rating_df[rating_df['movie_id'].isin(rating_df_grouped.values)]
    # raise Exception(rating_df)
    count = 0
    with transaction.atomic():  # with終わるまで書き込みしない
        for _, (uid, mid, rating, _) in rating_df.iterrows():
            # count += 1
            # if count < 3000:
            # if rating.count() > 10:
            user_profile = UserProfile.objects.get(uid=uid)  # UserProfileクラスのuidをとってくる
            movie = Movie.objects.get(mid=mid)  # Movieクラスのmidをとってくる
            ratings = Rating.objects.create(user_profile=user_profile, movie=movie,
                                            score=rating)  # 上でとっているidをRatingクラスに入れる(紐付ける)
            task = DataUploadTask.objects.get(tid=self.request.id)
            count += 1
            logger.info("updateの割合 %s" % str(count/rating_length))
            logger.info("1番目 %s" % task)
            task.state = 'DataUploadが完了しました。'
            task.save()
            ratings.save()
    return 0


