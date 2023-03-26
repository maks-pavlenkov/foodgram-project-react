from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
    ADMIN = 'admin'
    USER = 'user'

    ROLES = [
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь')
    ]
    username = models.CharField(
        verbose_name='Почтовый ящик',
        max_length=150,
        unique=True)
    email = models.EmailField(
        max_length=254)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        null=True)
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        null=True)
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
