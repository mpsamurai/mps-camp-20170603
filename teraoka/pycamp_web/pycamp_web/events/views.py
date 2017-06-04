from django.shortcuts import render, redirect
from django.views import View
from events import models   #モデルをインポート
from documents.models import Document
from django.http import HttpResponse   # httpのレスポンスを返す
from django.http import Http404


class EventListView(View):


    def get(self, request):  # 情報をきたら
        x = None
        # events = models.Event.objects.all()  # Eventモデルのインスタンス objects.all()は全て取得 Event.documents.all でイベントのドキュメントを全部取得できる
        events = models.Event.objects.all()
        # raise Exception("event", [i for i in documents])

        #return HttpResponse((['%s %s %s %s<br>' % (event.title, event.detail, event.start, event.end) for event in events]))   # OKを返すビューを作った
        return render(request, 'events/events_list.html', {'events': events})



class EventDetailView(View):  # イベントの詳細ページを取得
    def get(self, request, event_id):
        try:
            event = models.Event.objects.get(id=event_id)
            return render(request, 'events/events_detail.html', {'event': event})
        except models.Event.DoesNotExist:
             #raise Http404
            return redirect('events:list')