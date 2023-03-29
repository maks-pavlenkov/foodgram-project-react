import os

from django.core.management import BaseCommand
from recipies.models import Ingredient
from .validators import data_validation


class Command(BaseCommand):
    help = "Наполняет базу данными из csv"

    def handle(self, *args, **options):
        counter = 0
        user_path = os.path.join(
            os.path.abspath(os.path.dirname('README.md')),
            'data/ingredients.csv'
        )
        data = data_validation(user_path)
        for row in data[1:]:
            if not Ingredient.objects.filter(name=row[0]).exists():
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1],
                )
            counter += 1
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {counter} records')
        )
