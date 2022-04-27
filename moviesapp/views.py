from django.shortcuts import render
from moviesapp.models import Movie


# Create your views here.
def home(request):
    movies = Movie.objects.all()
    context = {
        "movies": movies
    }
    return render(request=request,template_name="moviesapp/home.html",context=context)
