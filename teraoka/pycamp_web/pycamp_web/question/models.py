from django.db import models
# from events.models import Event
from django.contrib.auth.models import User  # user名、id、セッションなど持っている

# ここでDBへの定義をする
class Question(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    user = models.ForeignKey(User, related_name='questions')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.title

class Comment(models.Model):
    question = models.ForeignKey(Question, related_name='comments')  # Questionと紐づいている
    user = models.ForeignKey(User, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.title