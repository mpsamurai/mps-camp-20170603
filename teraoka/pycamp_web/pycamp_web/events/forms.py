from django import forms  # フォームを自動生成する
from events import models


# フォームを自動生成
class EventQuestionForm(forms.ModelForm): #Modelを勝手に読み込む
    class Meta:  # class Metaとは上記の(EventQuestionFormクラス)動作を決めるクラスのこと
        model = models.EventQuestion   #どのmodelを読み込むか?フォームを自動で生成します
        # ユーザーに対して見せる項目を決める
        fields = ['title', 'detail']

