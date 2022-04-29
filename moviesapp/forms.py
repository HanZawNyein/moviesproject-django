from django import forms
from django.forms import BaseModelFormSet

from moviesapp.models import Movie, MovieImage


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ('slug',)
