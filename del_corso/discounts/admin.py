from django.contrib import admin

from discounts.models import Discount, ProductDiscount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ("name", "discount_price", "start_date", "end_date")
    search_fields = ("id", "name", "discount_price")


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    model = ProductDiscount
    list_display = ("product", "discount")
    search_fields = ("product__name", "discount__name", "discount__discount_price")
