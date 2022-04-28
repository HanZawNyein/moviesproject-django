from django.urls import path
from moviesapp import views

app_name = "movies_app"

urlpatterns = [
    path('', views.home, name="home"),
    path('<str:movie_type>/<slug:slug>/<int:year>/<int:month>/<int:day>/<int:second>', views.detail, name="details"),
    path('movies/',views.movies,name="movies"),
    path('series/',views.series,name="series")
]
