from django.http import HttpResponseRedirect
from django.shortcuts import render
from rating.form import UploadFileForm
from django.views import View


class DataUploadView(View):

    def get(self, request):
        return render(request, 'rating/data_upload.html', {})

    def post(self, request):
        return render(request, 'rating/upload_complete.html', {})


class MovieDataUpload(View):

    def upload_file(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST)
            if form.is_valid():
                f = request.FILES['data-file']
                # raise Exception("F", f)
                # return HttpResponseRedirect('/success/url/')
        else:
            form = UploadFileForm()
        return render(request, 'rating/upload_complete.html', {'form': form})
