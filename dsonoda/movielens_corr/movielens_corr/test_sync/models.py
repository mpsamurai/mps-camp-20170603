from django.db import models

# Create your models here.

class SyncStatus(models.Model):
    queue_id = models.CharField(max_length=50)
    status = models.IntegerField()
