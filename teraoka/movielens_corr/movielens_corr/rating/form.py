from django import forms
from rating import models

class UploadFileForm(forms.ModelForm):
    """
    フォームを通す意味は「バリデーションチェック」不正入力を防ぐ
    # や、int型なのに文字列をチェックなどしてくれるので
    # Dataを受け取るだけの目的ならこれ使う必要はない。
    """
    class Meta:
        model = models.Movie
        title = forms.CharField(max_length=50)
        file = forms.FileField()
        fields = ['title']