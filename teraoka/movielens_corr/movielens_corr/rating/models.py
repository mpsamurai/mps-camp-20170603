from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class User(models.Model):
    user = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)

    def __str__(self):
        return self.user

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings')
    user = models.ForeignKey(User, related_name='own_ratings')
    score = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.movie.title, self.score)