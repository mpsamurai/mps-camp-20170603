from django import forms

class DataUpForm(forms.Form):
    movie_file = forms.FileField()
    rating_file = forms.FileField()
    user_file = forms.FileField()
