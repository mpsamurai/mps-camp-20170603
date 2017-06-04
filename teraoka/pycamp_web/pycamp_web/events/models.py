from django.db import models
from documents.models import Document
from question.models import Question

# ここでDBへの定義をする
class Event(models.Model):
    title = models.CharField(max_length=255)
    documents = models.ManyToManyField(Document, related_name='events',  blank=True)
    detail = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
       return self.title   # この戻り値がtitleとして表示される(時刻情報もね)


class EventQuestion(Question):
    event = models.ForeignKey(Event, related_name='questions')

    def __str__(self):
       return self.title   # この戻り値がtitleとして表示される(時刻情報もね)
