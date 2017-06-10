from django.db import models


# Create your models here.
class Movie(models.Model):
    mid = models.IntegerField(unique=True) # models.IntegerField(unique=True)は同じ値が入ってきたらエラー
    title = models.CharField(max_length=255)
    # models.Movie.objects.update_or_create(mid=mid, default={_,_})  これならupdate対応
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/  [update_or_createで検索するとでる]
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    uid = models.IntegerField(unique=True)
    gender = models.CharField(max_length=255)

    def __str__(self):
        return str(self.uid)

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings')  # ForeignKeyはint型です
    user_profile = models.ForeignKey(UserProfile, related_name='own_ratings')  # ForeignKeyはint型です
    score = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.movie.title, self.score)

class DataUploadTask(models.Model):
    state = models.CharField(max_length=255)
    tid = models.CharField(max_length=255)
    # progress = models.TextField(null=True)
    def __str__(self):
        return self.state