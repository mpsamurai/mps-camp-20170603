from django.http import HttpResponse
from task import tasks
from django.views import View


#タスクをローカルで実行
class AddWithSleepSyncView(View):

    def get(self, request):
        r = tasks.add_with_sleep.apply((2, 3))
        return HttpResponse('The answer is %s' % r.get())


class AddWithSleepAsyncView(View):
    def get(self, request):
        r = tasks.add_with_sleep.delay(2, 3)
        return HttpResponse('The task is queued %s' % r)
