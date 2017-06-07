from django.db import models


# Create your models here.
class Movie(models.Model):
    mid = models.IntegerField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    uid = models.IntegerField()
    gender = models.CharField(max_length=255)

    def __str__(self):
        return self.user

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings')  # ForeignKeyはint型です
    user_profile = models.ForeignKey(UserProfile, related_name='own_ratings')  # ForeignKeyはint型です
    score = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.movie.title, self.score)