from django.shortcuts import render, get_object_or_404
from moviesapp.models import Movie


# Create your views here.
def home(request):
    all_movies = Movie.objects.all().order_by("-created")
    context = {
        "movies": all_movies
    }
    return render(request=request, template_name="moviesapp/home.html", context=context)


def detail(request, movie_type, slug, year, month, day, second):
    movie = get_object_or_404(Movie, slug=slug, type=movie_type, created__year=year, created__month=month,
                              created__day=day, created__second=second)
    context = {
        "movie": movie
    }
    return render(request=request, template_name="moviesapp/detail.html", context=context)


def movies(request):
    all_movies = Movie.movies.all()
    context = {
        "movies": all_movies
    }
    return render(request=request, template_name="moviesapp/home.html", context=context)

def series(request):
    all_movies = Movie.series.all()
    context = {
        "movies": all_movies
    }
    return render(request=request, template_name="moviesapp/home.html", context=context)
