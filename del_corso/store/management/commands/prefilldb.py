from django.core.management.base import BaseCommand

from store.management.builder import PreFillDbBuilder


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = ["Ботинки", "Кеды", "Кроссовки", "Лоферы", "Туфли", "Сапоги"]
        sizes = (35, 41)
        seasons = ["Зима", "Весна", "Лето", "Осень", "Деми"]
        colors = ["Красный", "Белый", "Черный", "Бежевый", "Розовый", "Серый"]

        PreFillDbBuilder(categories=categories, sizes=sizes, seasons=seasons, colors=colors)

