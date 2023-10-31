from django.core.management.base import BaseCommand

from store.management.builder import PopulateDbBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):

        PopulateDbBuilder()
        self.stdout.write("The database populated successfully!")
