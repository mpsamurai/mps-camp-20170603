from movielens_corr.celery import app as celery_app
from celery.utils.log import get_task_logger
# from task.views import TaskStart
from task.models import TaskTable
from django.shortcuts import render


logger = get_task_logger(__name__)



@celery_app.task(bind=True)
def add_with_sleep(self, x, y):

    import time
    time.sleep(3)
    r = x + y

    logger.info('The answer is %s' % r)
    taskTable = TaskTable.objects.get(tid=self.request.id)
    taskTable.score = r
    taskTable.state = '終わりました'

    taskTable.save()

    return r
