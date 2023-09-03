from django.contrib import admin

from store.models import Product, ProductImage, SeasonCategory, Size, TypeCategory, Color


class ProductAdmin(admin.ModelAdmin):
    model = Product


class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage


class SeasonCategoryAdmin(admin.ModelAdmin):
    model = SeasonCategory


class SizeAdmin(admin.ModelAdmin):
    model = Size


class TypeCategoryAdmin(admin.ModelAdmin):
    model = TypeCategory


class ColorAdmin(admin.ModelAdmin):
    model = Color


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(SeasonCategory, SeasonCategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(TypeCategory, TypeCategoryAdmin)
admin.site.register(Color, ColorAdmin)
