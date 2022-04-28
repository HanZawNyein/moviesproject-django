# Generated by Django 3.2.13 on 2022-04-28 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0004_rename_movietype_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.ManyToManyField(related_name='category_of_movies', to='moviesapp.Category'),
        ),
    ]
