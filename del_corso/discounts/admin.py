from django.contrib import admin

from discounts.models import Discount, ProductDiscount


class DiscountAdmin(admin.ModelAdmin):
    model = Discount


class ProductDiscountAdmin(admin.ModelAdmin):
    model = ProductDiscount


admin.site.register(Discount, DiscountAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
