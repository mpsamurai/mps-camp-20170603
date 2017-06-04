from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    uploaed = models.FileField(upload_to='uploads/%Y/%m/%d/')
    # updated = models.DateTimeField(auto_now=True)
    detail = models.TextField()
    start = models.DateTimeField()

    def __str__(self):
       return self.title   # この戻り値がtitleとして表示される(時刻情報もね)
