import os

from django.core.management import BaseCommand
from recipies.models import Ingredient

from .validators import data_validation


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            'data/ingredients.csv'
        )
        required_fields_users = [
            'id',
            'name',
            'units'
        ]
        data = data_validation(user_path, required_fields_users)
        for row in data[1:]:
            Ingredient.objects.create(
                id=row[0],
                units=row[1],
            )
