from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from moviesapp.models import Movie, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


# Create your views here.
@login_required
def home(request, type=None, slug=None):
    all_movies = None
    categories = Category.objects.all()
    if not type:
        all_movies = Movie.objects.all().order_by("-created")
    elif type == "movies":
        all_movies = Movie.movies.all().order_by("-created")
    elif type == "series":
        all_movies = Movie.series.all().order_by("-created")

    if request.method == "POST":
        all_movies = Movie.objects.filter(name__contains=request.POST['search']).order_by('-created')

    if slug:
        all_movies = Category.objects.get(slug=slug).category_of_movies.all()

    # pagination
    paginator = Paginator(all_movies, 2)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        all_movies = paginator.page(page)
    except PageNotAnInteger:  # If page is not an integer deliver the first page
        all_movies = paginator.page(1)
    except EmptyPage:  # If page is out of range deliver last page of results
        all_movies = paginator.page(paginator.num_pages)

    context = {
        "movies": all_movies,
        "categories": categories,
        "page": page
    }
    return render(request=request, template_name="moviesapp/home.html", context=context)


@login_required
def detail(request, movie_type, slug, year, month, day, second):
    movie = get_object_or_404(Movie, slug=slug, type=movie_type, created__year=year, created__month=month,
                              created__day=day, created__second=second)
    categories = Category.objects.all()
    context = {
        "movie": movie,
        "categories": categories
    }
    return render(request=request, template_name="moviesapp/detail.html", context=context)


@login_required
def movie_list_by_category(request, slug):
    category = Category.objects.get(slug=slug).category_of_movies.all()
    categories = Category.objects.all()
    context = {
        "movies": category,
        "categories": categories
    }
    return render(request=request, template_name="moviesapp/home.html", context=context)


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("movies_app:home")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        login_form = LoginForm()
    return render(request, 'moviesapp/authentication/login.html', {'login_form': login_form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("movies_app:user_login")
