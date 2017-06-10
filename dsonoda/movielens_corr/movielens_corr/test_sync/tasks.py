from movielens_corr.celery import app as celery_app
from celery.utils.log import get_task_logger
from test_sync import models

logger = get_task_logger(__name__)

#celery のタスク化
@celery_app.task(bind=True)
def add_with_sleep(self):
    """
    Celery のタスク
    :param self:
    :return:
    """

    import time

    # ステータス 2: なんらかの計算中
    sync_status = models.SyncStatus.objects.get(queue_id=self.request.id)
    sync_status.status=2
    sync_status.save()

    # なんらかの計算
    time.sleep(20)

    # ステータス 3: 計算完了
    sync_status = models.SyncStatus.objects.get(queue_id=self.request.id)
    sync_status.status=3
    sync_status.save()

    return task_id