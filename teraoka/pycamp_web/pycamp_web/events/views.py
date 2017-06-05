from django.shortcuts import render, redirect

from django.views import View
from events import models
from documents.models import Document
from django.http import HttpResponse   # httpのレスポンス機能module
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # ページネーション機能module
from events.models import EventQuestion
from events import forms
from django.contrib.auth.decorators import login_required  #  アクセス権限
from django.utils.decorators import method_decorator  # アクセス権限

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

    # def get(self, request):  # 情報をきたら
    #     x = None
    #     # events = models.Event.objects.all()  # Eventモデルのインスタンス objects.all()は全て取得 Event.documents.all でイベントのドキュメントを全部取得できる
    #     events = models.Event.objects.all()
    #     # raise Exception("event", [i for i in documents])
    #     p = Paginator(events, 20)
    #     p_page = int(request.GET.get("p", 1))
    #     page = p.page(p_page)
    #     events = page.object_list
    #     # raise Exception(events)
    #     pages = []
    #     for i in range(-3, 4):
    #         if p_page > 5:
    #             pages.append(i+p_page) # 3,4,5,6,7,8,9
    #             # raise Exception(pages)
    #         elif p_page > 30:
    #             pages.append(p_page)
    #             break

    def get(self, request):  # 情報をきたら
        events = models.Event.objects.all()
        paginator = Paginator(events, 20)

        now_page = int(request.GET.get("p", 1))
        page = paginator.page(now_page)
        events = page.object_list

        pages = []
        for i in range(-3, 4):
            try:
                contacts = paginator.page(now_page)  # paginator.pageにより1000個(20個分割)、1~50ページ取得contacts変数へ
                pages = []

                after_p_num = 3  # 現在ページNo前後の表示ページ数
                start_page = 1  # 表示開始ページNo
                end_page = (after_p_num * 2) + 2  # 表示終了ページNo
                if now_page - after_p_num < 1:
                    start_page = 1  # 表示開始ページNo
                    end_page = (after_p_num * 2) + 2  # 表示終了ページNo
                elif now_page + after_p_num > paginator.num_pages:
                    start_page = paginator.num_pages - after_p_num * 2
                    end_page = paginator.num_pages + 1
                else:
                    start_page = now_page - after_p_num
                    end_page = now_page + after_p_num + 1
                for p in range(start_page, end_page):
                    pages.append(p)

            except PageNotAnInteger:  # now_pageが整数値でなければ最初のpageを返す
                events = paginator.page(1)  # pageじゃないの？

            except EmptyPage:  # ページが範囲外（たとえば9999）の場合、結果の最終ページを返す
                events = paginator.page(paginator.num_pages)  # <Page 50 of 50>状態を返す
        # raise Exception(pages) [44, 45, 46, 47, 48, 49, 50] 表示

        #return HttpResponse((['%s %s %s %s<br>' % (event.title, event.detail, event.start, event.end) for event in events]))   # OKを返すビューを作った
        return render(request, 'events/events_list.html', {'events': events, "pagination": pages})  # {'events': events}右側のeventsで情報を渡している


class EventDetailView(View):  # イベントの詳細ページを取得
    def get(self, request, event_id):
        try:
            event = models.Event.objects.get(id=event_id)
            event_questions = models.EventQuestion.objects.filter(event__id = event_id)
            form = forms.EventQuestionForm()

            return render(request, 'events/events_detail.html', {'event': event, 'event_questions': event_questions, 'form':form})

        except models.Event.DoesNotExist:
             #raise Http404
            return redirect('events:list')

    #  フォームは見えるけど、投稿はできない！ようにする(ログインしないと)
    @method_decorator(login_required)  # ビューが必ず持っているリクエストを受け取るか(ログインをしている人しか受け取ったらダメ)
    def post(self, request, event_id):
        form = forms.EventQuestionForm(request.POST) #postされたデータを取得している-> formへ入れている
        # インスタンスを作成する
        if form.is_valid():  # 変な情報がないことを保証する場合
            event_question = form.save(commit = False) # インスタンスだけ生成してDBには入れない(commit = False)
            event_question.user = request.user
            event_question.event = models.Event.objects.get(id=event_id)
            event_question.save()  # これはDBにsave()

            return self.get(request, event_id)

@method_decorator(login_required, "dispatch")  # ログイン確認を全体にかける場合は"dispatch"が必要
class EventBookingView(View):  # 予約モデル
    def get(self, request):
        try:   #  requestにはたくさん情報ありUserが今リクエストきているuserだけを取得してfilterをかけてくれている
            event_booking = models.Booking.objects.filter(user = request.user)  # eventのidを取得
            # raise Exception(event_booking)
            return render(request, 'events/events_detail.html', {'event_booking': event_booking})

        except models.Event.DoesNotExist:
             #raise Http404
            return redirect('events:list')

