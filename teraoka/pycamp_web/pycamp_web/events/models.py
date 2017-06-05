from django.db import models
from documents.models import Document
from question.models import Question
from django.contrib.auth.models import User


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


class EventBookingList(models.Model):
    name = models.CharField(max_length=255)  # 受講者
    event = models.ForeignKey(Event, related_name='bookings')  # Questionと紐づいている
    user = models.ForeignKey(User, related_name='own_bookings')
    updated = models.DateTimeField(auto_now=True)  # 予約した日
    is_canceld = models.BooleanField(default=False)  # キャンセルフラク
    def __str__(self):
       return self.name   # この戻り値がtitleとして表示される

# Booking
# イベント
# 受講者
# 予約した日(キャンセルフラグを入れておく)：システムのuserには見せない
# 　
# model
# template
# get(event)
#
# post
# form
# postメソッド
#
# キャンセル