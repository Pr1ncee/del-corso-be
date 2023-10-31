from django.contrib import admin

from store.models import ProductImage


class ProductImageAdminInline(admin.TabularInline):
    model = ProductImage
    extra = 5
