# Generated by Django 2.2.16 on 2023-03-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20230309_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('user', 'Пользователь')], default='user', max_length=50),
        ),
    ]