from sys import stdout

from store.models import TypeCategory, Size, SeasonCategory, Color


class PreFillDbBuilder:
    def __init__(self, categories: list[str], sizes: tuple[int, int], seasons: list[str], colors: list[str]):
        self.create_categories(categories=categories)
        self.create_sizes(*sizes)
        self.create_seasons(seasons=seasons)
        self.create_colors(colors=colors)

    def create_categories(self, categories: list[str]) -> None:
        type_category_objs = [TypeCategory(name=category) for category in categories]
        TypeCategory.objects.bulk_create(type_category_objs)
        stdout.write("Shoes categories have been successfully created!\n")

    def create_sizes(self, size_min: int, size_max: int) -> None:
        size_list = list(range(size_min, size_max + 1))

        size_objs = [Size(size=size) for size in size_list]
        Size.objects.bulk_create(size_objs)
        stdout.write("Sizes have been successfully created!\n")

    def create_seasons(self, seasons: list[str]) -> None:
        season_objs = [SeasonCategory(name=season) for season in seasons]
        SeasonCategory.objects.bulk_create(season_objs)
        stdout.write("Seasons have been successfully created!\n")

    def create_colors(self, colors: list[str]) -> None:
        color_objs = [Color(color=color) for color in colors]
        Color.objects.bulk_create(color_objs)
        stdout.write("Colors have been successfully created!\n")
