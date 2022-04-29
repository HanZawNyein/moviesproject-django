from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from moviesapp.models import Movie, Category, MovieImage, Drive
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from moviesapp.forms import LoginForm, MovieForm
from django.utils.text import slugify

# Create your views here.
from moviesapp.telegrambot import post_to_telegram_channel


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
    movie_category_ids = movie.category.values_list('id', flat=True)
    related_movies = Movie.objects.filter(category__in=movie_category_ids).exclude(id=movie.id).order_by('-created')
    context = {
        "movie": movie,
        "categories": categories,
        "related_movies": related_movies
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


# create
def add_movies(request):
    movie_image_form = modelformset_factory(MovieImage, fields=('image',), extra=3)
    movie_drive_name = modelformset_factory(Drive, fields=('drive_link', 'drive_type', 'series_name'), extra=3)

    if request.method == "POST":
        movie_form = MovieForm(request.POST or None)
        movie_image_formset = movie_image_form(request.POST or None, request.FILES or None)
        movie_drive_name_formset = movie_drive_name(request.POST or None)
        #
        # print("movie_form --->", movie_form.is_valid())
        # print("movie_image_formset --->", movie_image_formset.is_valid())
        # print("movie_drive_name_formset --->", movie_drive_name_formset.is_valid())
        if movie_form.is_valid() and movie_image_formset.is_valid() and movie_drive_name_formset.is_valid():
            movie = movie_form.save(commit=False)
            movie.slug = slugify(movie.name)
            movie.save()
            movie_form.save_m2m()

            for instance in movie_image_formset:
                try:
                    image = MovieImage(movie_name=movie, image=instance.cleaned_data['image'])
                    image.save()
                except:
                    pass

            for movie_drive in movie_drive_name_formset:
                try:
                    movie_drive = Drive(movie_name=movie)
                    movie_drive.save()
                except:
                    pass
            context = {
                "movie": movie,
                "movie_image": movie.movie_of_images.all()[0].image.path
            }
            post_to_telegram_channel(template="moviesapp/telegram/send_to_telegram_channel.html", context=context)
            return redirect("movies_app:home")
    else:
        movie_image_form = movie_image_form(queryset=MovieImage.objects.none())
        movie_form = MovieForm()
        movie_drive_name = movie_drive_name(queryset=Drive.objects.none())

    context = {
        "movie_form": movie_form,
        "movie_image_form": movie_image_form,
        "movie_drive_name": movie_drive_name
    }
    return render(request=request, template_name="moviesapp/crud/add_movies.html", context=context)
