from django.contrib import admin
from moviesapp.models import Movie, MovieImage, Drive, DriveName, Comment


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type', 'created')
    list_filter = ('name', 'type', 'created')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('created',)


@admin.register(DriveName)
class DriveNameAdmin(admin.ModelAdmin):
    list_display = ('drive_name', 'created')
    list_filter = ('drive_name', 'created')
    ordering = ('created',)


@admin.register(Drive)
class DriveAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'drive_link', 'drive_type', 'created')
    list_filter = ('movie_name', 'drive_type', 'created')
    ordering = ('created',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'comment', 'created')
    list_filter = ('movie_name', 'comment', 'created')
    ordering = ('created',)


@admin.register(MovieImage)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'created')
    list_filter = ('movie_name', 'created')
    ordering = ('created',)
