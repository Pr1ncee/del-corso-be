from django.contrib import admin

from banners.models import BannerImage


@admin.register(BannerImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = BannerImage
    list_display = ("main", "season_category")
