from django.db import models
from d3js_graph_movie_rating import consts

class Movie(models.Model):
    """
    映画情報
    """
    mid = models.IntegerField()
    title = models.CharField(max_length=100)

class Rating(models.Model):
    """
    映画のレーティング
    """
    user_info = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.IntegerField()

class UserInfo(models.Model):
    """
    ユーザ情報
    """
    uid = models.IntegerField()
    gender = models.CharField(max_length=1, choices=consts.GENDER_CHOISE)

class SyncStatus(models.Model):
    """
    並列処理のステータス管理
    """
    queue_id = models.CharField(max_length=50)
    mode = models.IntegerField(choices=consts.SYNC_MODE)
    status = models.IntegerField(choices=consts.SYNC_STATUS)