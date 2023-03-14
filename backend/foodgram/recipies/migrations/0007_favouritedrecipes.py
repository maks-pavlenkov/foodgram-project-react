# Generated by Django 2.2.16 on 2023-03-12 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipies', '0006_auto_20230311_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouritedRecipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipies.Recipe')),
            ],
        ),
    ]