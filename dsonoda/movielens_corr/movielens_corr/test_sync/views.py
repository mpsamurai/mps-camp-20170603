from django.views import View
from django.shortcuts import render
from test_sync import models
from test_sync import tasks
from django.http import HttpResponse

# Create your views here.

class pushQueueView(View):
    def get(self, request):
        """
        Celery にキューを投げる
        """

        # 並列に実行
        # delay() 、つまりCeleryにタスクが投げられる
        r = tasks.add_with_sleep.delay()

        # ステータス 1: Celery にタスクを投げる
        obj = models.SyncStatus.objects.create(queue_id=r.task_id,status=1)

        return render(request, 'test_sync/push_queue.html', {})

class viewQueueView(View):
    """
    キューの一覧を表示
    """
    def get(self, request):
        return render(request, 'test_sync/view_queue.html', {'sync_status_list': models.SyncStatus.objects.all()})
