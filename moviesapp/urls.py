from django.urls import path
from moviesapp import views

app_name = "movies_app"

urlpatterns = [
    path('', views.home, name="home"),
    path('<str:type>/', views.home, name="movies_type"),
    path('<str:movie_type>/<slug:slug>/<int:year>/<int:month>/<int:day>/<int:second>', views.detail, name="details"),
    path('search/', views.home, name="search"),
    path('movies_list_by_categories/<slug:slug>/', views.home, name="movie_list_by_category")
]
