from django.contrib import admin

from store.models import Product, ProductImage, SeasonCategory, Size, TypeCategory, Color
from store.models.product import ProductSize


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("id", "name", "price", "vendor_code", "color", "season_categories", "type_category")
    search_fields = ("id", "name", "price", "vendor_code")

    def season_categories(self, obj):
        return ", ".join([str(category) for category in obj.season_category.all()])

    season_categories.short_description = "Сезон"


class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ("id", "product")


class ProductSizeAdmin(admin.ModelAdmin):
    model = ProductSize


class SeasonCategoryAdmin(admin.ModelAdmin):
    model = SeasonCategory


class SizeAdmin(admin.ModelAdmin):
    model = Size


class TypeCategoryAdmin(admin.ModelAdmin):
    model = TypeCategory
    list_display = ("id", "name", "is_popular")
    search_fields = ("id", "name")


class ColorAdmin(admin.ModelAdmin):
    model = Color
    list_display = ("id", "color")
    search_fields = ("id", "color")


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(SeasonCategory, SeasonCategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(TypeCategory, TypeCategoryAdmin)
admin.site.register(Color, ColorAdmin)
