from django.db import models
from questions.models import Question

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    documents = models.ManyToManyField(Document, related_name="events", blank=True)
    def __str__(self):
        return self.title

class EventQuestions(Question):
    event = models.ForeignKey(Event, related_name='questions')
    def __str__(self):
        return self.title