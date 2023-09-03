from django.contrib import admin

from discounts.models import Discount, ProductDiscount


class DiscountAdmin(admin.ModelAdmin):
    model = Discount
    list_display = ("name", "discount_price", "start_date", "end_date")
    search_fields = ("id", "name", "discount_price")


class ProductDiscountAdmin(admin.ModelAdmin):
    model = ProductDiscount
    list_display = ("product", "discount")


admin.site.register(Discount, DiscountAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
