# Generated by Django 3.2.13 on 2022-04-26 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0002_movieimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movieimage',
            name='image',
            field=models.ImageField(upload_to='movies/%Y/%m/%d'),
        ),
    ]
