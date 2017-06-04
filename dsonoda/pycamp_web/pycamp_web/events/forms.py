from django import forms
from events import models

class EventQuestionForm(forms.ModelForm):
    class Meta:
        model = models.EventQuestions
        fields = ['title', 'detail']