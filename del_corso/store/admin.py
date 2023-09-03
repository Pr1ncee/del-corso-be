from django.contrib import admin

from store.models import Product, ProductImage, SeasonCategory, Size, TypeCategory, Color


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("id", "name", "price", "vendor_code", "size", "color", "season_category", "type_category")
    search_fields = ("id", "name", "price", "vendor_code")


class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ("id", "product")


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
admin.site.register(SeasonCategory, SeasonCategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(TypeCategory, TypeCategoryAdmin)
admin.site.register(Color, ColorAdmin)
