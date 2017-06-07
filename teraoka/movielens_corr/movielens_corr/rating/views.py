from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
# from rating.form import UploadFileForm
from django.views import View
from rating.form import UploadFileForm
from rating.models import Movie
import pandas as pd
from io import BytesIO, StringIO
"""
BytesIOがfile
"""

class DataUploadView(View):

    def get(self, request):
        return render(request, 'rating/data_upload.html', {})

    def post(self, request):
        file = request.FILES["data-file"]
        movies = pd.read_csv(BytesIO(request.FILES["data-file"].read()),
                             sep='::', header=None,
                             names=['movie_id', 'title', 'genres'], encoding='ISO-8859-1')
        raise Exception(movies)
        # title = form.title

        # f = request.FILES['data-file']
        # f = form.read()
        # インスタンスにする
        # if form.is_valid():
        #     movie = form.save(commit=False)


            # f = request.FILES['data-file']
            # files = f.read()
        # return render(request, 'rating/upload_complete.html', {'files':f})
        return render(request, 'rating/upload_complete.html', {"form":form})

# class Test(View):
#
#     def get(self, request):
#         movie = Movie.objects.all()
#         title = movie[0]
#         # raise Exception(title)
#         return render(request, 'rating/rating_draw.html', {'title':title})
# class MovieDataUpload(View):
#     """
#     post
#     """
#     def upload_file(request):
#         if request.method == 'POST':
#             form = UploadFileForm(request.POST)
#             if form.is_valid():
#                 f = request.FILES['data-file']
#                 # raise Exception("F", f)
#                 # return HttpResponseRedirect('/success/url/')
#         else:
#             form = UploadFileForm()
#         return render(request, 'rating/upload_complete.html', {'form': form})
