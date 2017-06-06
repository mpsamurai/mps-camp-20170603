from django import forms
from rating import models

class UploadFileForm(forms.ModelForm):
    """
    Postされたらrequestデータを渡すクラス
    title: ファイル名
    file: data
    """
    class Meta:
        model = models.Movie
        # ユーザーへ見せる項目
        fields = ['title']
        # title = forms.CharField(max_length=50)
        # file = forms.FileField()