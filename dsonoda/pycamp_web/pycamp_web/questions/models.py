from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    user = models.ForeignKey(User, related_name = 'questions')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    user = models.ForeignKey(User, related_name = 'comments')
    question = models.ForeignKey(Question, related_name = 'comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title