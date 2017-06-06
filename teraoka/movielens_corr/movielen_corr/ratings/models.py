from django.db import models
import pandas as pd
"""
models.pyに読み込んで
sqlで統計処理
to_csvで書き出す-> views.pyで表示処理
クラスを構成する祭は
文章を組み立てることと同じなので
『主語(誰が)』『述語(何をする)』『修飾語(何を使って)』
Movieクラス
『
Ratingクラスの例
『userが』『点数をつける』『映画タイトルを使って(継承してる)』
"""

# クラス定義
class Movie(models.Model):
    """
    映画情報
    """
    title = models.CharField(max_length=255)
    def __str__(self):
       return self.title


class User(models.Model):
    """
    User情報(今回は男女がわかればいい)
    """
    user = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    def __str__(self):
        return self.title


class Ratings(models.Model):
    """
    どのUserが、どの映画を、何点つけたかを知りたい
    """
    user = models.ForeignKey(User, related_name='own_ratings',  blank=True)
    movie = models.ForeignKey(Movie, related_name='ratings',  blank=True)
    score = models.IntegerField()
    def __str__(self):
       return self.title


