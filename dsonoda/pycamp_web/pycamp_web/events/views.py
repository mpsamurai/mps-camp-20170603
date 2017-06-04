from django.shortcuts import render

# Create your views here.
from django.views import View

from events import models
from events import forms
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class EventListView(View):
    def get(self, request):
        events = models.Event.objects.all()
        paginator = Paginator(events, 25)

        page = request.GET.get('p', 1)
        page = int(page)
        try:
            events = paginator.page(page)

            # ページ表示番号リスト
            pages = []
            pre_after_p_num = 3                     #現在ページNo前後の表示ページ数
            view_start_page = 1                     #表示開始ページNo
            view_end_page = (pre_after_p_num * 2) + 2 #表示終了ページNo
            if page - pre_after_p_num < 1:
                view_start_page = 1  # 表示開始ページNo
                view_end_page = (pre_after_p_num * 2) + 2  # 表示終了ページNo
            elif page + pre_after_p_num > paginator.num_pages:
                view_start_page = paginator.num_pages - pre_after_p_num * 2
                view_end_page = paginator.num_pages + 1
            else:
                view_start_page = page - pre_after_p_num
                view_end_page = page + pre_after_p_num + 1
            for p in range(view_start_page, view_end_page):
                pages.append(p)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            events = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            events = paginator.page(paginator.num_pages)

        return render(request, 'events/list.html', {'events': events, 'pages': pages})

class EventDetailView(View):
    def get(self, request, event_id):
        try:
            #イベント
            event = models.Event.objects.get(id=event_id)
            #イベントに紐づく質問
            event_questions = models.EventQuestions.objects.filter(event__id=event_id)
            #イベントに紐づく質問フォーム
            form = forms.EventQuestionForm()
        except models.Event.DoesNotExist:
            #raise Http404
            return redirect("events:list")
        return render(request, 'events/detail.html', {'event': event, 'event_questions': event_questions, 'form': form})

    @method_decorator(login_required)
    def post(self, request, event_id):
        form = forms.EventQuestionForm(request.POST)
        if form.is_valid():
            event_question = form.save(commit = False)
            event_question.user = request.user
            event_question.event = models.Event.objects.get(id=event_id)
            event_question.save()
            return self.get(request, event_id)