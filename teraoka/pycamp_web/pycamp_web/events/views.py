from django.shortcuts import render, redirect
from django.views import View
from events import models   #モデルをインポート
from documents.models import Document
from django.http import HttpResponse   # httpのレスポンスを返す
from django.http import Http404
from django.core.paginator import Paginator  # ページネーションを作成する
from events.models import EventQuestion
from events import forms
from django.contrib.auth.decorators import login_required

# # ログをとる練習
# import logging
# # Get an instance of a logger
# logger = logging.getLogger(__name__)
#
# def my_view(request, arg1, arg):
#
#     if bad_mojo:
#         # Log an error message
#         logger.error('Something went wrong!')
#

class EventListView(View):


    def get(self, request):  # 情報をきたら
        x = None
        # events = models.Event.objects.all()  # Eventモデルのインスタンス objects.all()は全て取得 Event.documents.all でイベントのドキュメントを全部取得できる
        events = models.Event.objects.all()
        # raise Exception("event", [i for i in documents])
        p = Paginator(events, 20)
        p_page = int(request.GET.get("p", 1))
        page = p.page(p_page)
        events = page.object_list
        # raise Exception(events)
        pages = []
        for i in range(-3, 4):
            if p_page > 5:
                pages.append(i+p_page) # 3,4,5,6,7,8,9
                # raise Exception(pages)
            elif p_page > 30:
                pages.append(p_page)
                break

        #return HttpResponse((['%s %s %s %s<br>' % (event.title, event.detail, event.start, event.end) for event in events]))   # OKを返すビューを作った
        return render(request, 'events/events_list.html', {'events': events, "pagination": pages})  # {'events': events}右側のeventsで情報を渡している

# def get(request) このrequestの中にはたくさんの情報が入ってきている
#   urlの (127.0.0.1:8000/events/?p=3)など　get情報を取得する場合も使えます
#   page = request.GET.get("p", 1)  GETパラメーターを取得します、p の値　なければデフォルトは１ですよ

class EventDetailView(View):  # イベントの詳細ページを取得
    def get(self, request, event_id):
        try:
            event = models.Event.objects.get(id=event_id)
            event_questions = models.EventQuestion.objects.filter(event__id = event_id)
            form = forms.EventQuestionForm()
            # raise Exception(event_question)
            return render(request, 'events/events_detail.html', {'event': event, 'event_questions': event_questions, 'form':form})

        except models.Event.DoesNotExist:
             #raise Http404
            return redirect('events:list')


    def post(self, request, event_id):
        form = forms.EventQuestionForm(request.POST) #postされたデータを取得している-> formへ入れている
        # インスタンスを作成する
        if form.is_valid():  # 変な情報がないことを保証する場合
            event_question = form.save(commit = False) # インスタンスだけ生成してDBには入れない(commit = False)
            event_question.user = request.user
            event_question.event = models.Event.objects.get(id=event_id)
            event_question.save()  # これはDBにsave()

            return self.get(request, event_id)