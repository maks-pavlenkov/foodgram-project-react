# Generated by Django 2.2.16 on 2023-03-27 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0004_auto_20230327_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='images', verbose_name='Изображение рецепта'),
        ),
    ]
