# Generated by Django 2.2.16 on 2023-03-12 08:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipies', '0007_favouritedrecipes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavouritedRecipes',
            new_name='FavoritedRecipes',
        ),
    ]