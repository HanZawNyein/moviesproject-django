from django.db import models


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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class DriveName(models.Model):
    drive_name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.drive_name


class Drive(models.Model):
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_of_drives")
    drive_link = models.URLField(max_length=200)
    drive_type = models.ForeignKey(DriveName, on_delete=models.CASCADE)
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
