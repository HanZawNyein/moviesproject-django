from django.db import models
from django.urls import reverse


class MovieManager(models.Manager):
    def get_queryset(self):
        return super(MovieManager, self).get_queryset().filter(type='movies').order_by("-created")


class SeriesManager(models.Manager):
    def get_queryset(self):
        return super(SeriesManager, self).get_queryset().filter(type='series').order_by("-created")


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('movies_app:movie_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField()
    MOVIES_TYPE = (
        ('movies', 'Movies'),
        ('series', 'Series')
    )
    type = models.CharField(max_length=50, choices=MOVIES_TYPE)
    review = models.TextField()
    production_date = models.IntegerField(blank=True,default=2022)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name="category_of_movies")
    objects = models.Manager()
    movies = MovieManager()
    series = SeriesManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('movies_app:details',
                       args=[self.type, self.slug, self.created.year,
                             self.created.month, self.created.day, self.created.second])


class DriveName(models.Model):
    drive_name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.drive_name


class Drive(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_of_drives")
    drive_link = models.URLField(max_length=200)
    drive_type = models.ForeignKey(DriveName, on_delete=models.CASCADE)
    series_name = models.CharField(max_length=500,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.movie_name.name


class Comment(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_of_comments")
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.movie_name.name


class MovieImage(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_of_images")
    image = models.ImageField(upload_to="movies/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.movie_name.name