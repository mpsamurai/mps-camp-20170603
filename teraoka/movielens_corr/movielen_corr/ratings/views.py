from django.shortcuts import render
from django.views import View
from ratings import models
"""
ダウンロード(models.py)
正規化(views.py)
相関をとる(views.py)
D3.jsで描画(tenplates/movielen.html)
"""
# Create your views here.
class RatingsView(View):

    def get(self, request):  # request情報取得
        ratings = models.Ratings.objects.all()

        return render(request, 'ratings/ratings_list.html', {'ratings': ratings})