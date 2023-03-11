from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']

    username = models.CharField(
        max_length=150,
        unique=True)
    email = models.EmailField(
        max_length=254)
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True)
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True)

    def __str__(self):
        return self.username
