from django.urls import path
from moviesapp import views

app_name = "movies_app"

urlpatterns = [
    path('', views.home, name="home")
]
