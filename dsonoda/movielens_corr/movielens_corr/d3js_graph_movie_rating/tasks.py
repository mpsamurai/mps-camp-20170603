from movielens_corr.celery import app as celery_app
from celery.utils.log import get_task_logger
from d3js_graph_movie_rating import models
from d3js_graph_movie_rating import consts
from d3js_graph_movie_rating import tasks
from django.db import transaction
from django.db.models import Avg
from io import StringIO
import pandas as pd
import json

logger = get_task_logger(__name__)

@celery_app.task(bind=True)
def fileupload(self, files, queue_id):
    """
    ファイルアップロード
    :param self:
    :param files:
    :return:
    """
    # jsonデータのロード
    files = json.loads(files)

    # ファイルを受け取り
    movie_data = pd.read_csv(StringIO(files['movie']),
        sep='::',
        header=None,
        names=['mid', 'title', 'genres'],
        encoding='ISO-8859-1')
    user_data = pd.read_csv(StringIO(files['user_info']),
        sep='::',
        header=None,
        names=['uid', 'gender', 'age', 'occupation', 'zip'],
        encoding='ISO-8859-1')
    rating_data = pd.read_csv(StringIO(files['rating']),
        sep='::',
        header=None,
        names=['uid', 'mid', 'rating', 'timestamp'],
        encoding='ISO-8859-1')

    try:
        # transaction
        with transaction.atomic():
            # ステータス登録 2: 処理中
            sync_status = models.SyncStatus.objects.select_for_update().get(queue_id=queue_id)
            sync_status.status = consts.SYNC_STATUS[1][0]
            sync_status.save()

            # DB格納
            for i, (mid, title, genres) in movie_data.iterrows():
                obj = models.Movie.objects.create(
                    mid=mid,
                    title=title)

            for i, (uid, gender, age, occupation, zip_code) in user_data.iterrows():
                obj = models.UserInfo.objects.create(
                    uid=uid,
                    gender=gender)

            # レーティング情報は多すぎるため任意の件数でカット
            cnt = 6000
            for i, (r_uid, r_mid, rating, timestamp) in rating_data.iterrows():
                movie = models.Movie.objects.get(mid=r_mid)
                user_info = models.UserInfo.objects.get(uid=r_uid)
                obj = models.Rating.objects.create(user_info=user_info, movie=movie, rating=rating)
                if cnt == 0:
                    break
                cnt -= 1

            # ステータス登録 3: 処理完了
            sync_status = models.SyncStatus.objects.select_for_update().get(queue_id=queue_id, mode=consts.SYNC_MODE[0][0])
            sync_status.status = consts.SYNC_STATUS[2][0]
            sync_status.save()
    except:
        # ステータス登録 4: 処理失敗
        sync_status = models.SyncStatus.objects.select_for_update().get(queue_id=queue_id)
        sync_status.status = consts.SYNC_STATUS[3][0]
        sync_status.save()

    return queue_id


#celery のタスク化
@celery_app.task
def add_with_sleep(x,y):
    import time
    time.sleep(60)
    r = x + y
    logger.info('The answer is %s' % r)
    return r