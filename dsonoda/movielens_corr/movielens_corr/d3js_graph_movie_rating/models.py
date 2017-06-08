from django.db import models

# Create your models here.

# class MovieGenre(models.Model):
#     mid =
#     genre =

class Movie(models.Model):
    mid = models.IntegerField()
    title = models.CharField(max_length=100)
    # genres =

class Rating(models.Model):
    user_info = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.IntegerField()

class UserInfo(models.Model):
    GENDER_CHOISE = (('F', 'Female'), ('M', 'Male'))
    uid = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOISE)
    # age =
    # occupation =
    # zip_code =
