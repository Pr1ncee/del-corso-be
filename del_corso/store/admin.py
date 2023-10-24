from django.contrib import admin, messages
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html

from store.forms import BulkUpdateProductSizeForm, BulkUpdateProductColorForm
from store.models import Product, ProductImage, SeasonCategory, Size, TypeCategory, Color
from store.models.product import ProductSize


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        "id",
        "name",
        "price",
        "vendor_code",
        "color",
        "season_categories",
        "type_category",
        "in_stock",
        "size"
    )
    search_fields = ("id", "name", "price", "vendor_code")
    actions = ["set_in_stock", "set_out_of_stock"]

    def season_categories(self, obj):
        return ", ".join([str(category) for category in obj.season_category.all()])

    season_categories.short_description = "Сезон"

    @admin.action(description="В наличии")
    def set_in_stock(self, request, queryset):
        queryset.update(in_stock=True)
        self.message_user(request, f"Выбранные {queryset.count()} товары теперь в наличии.")

    @admin.action(description="Распродано")
    def set_out_of_stock(self, request, queryset):
        queryset.update(in_stock=False)
        self.message_user(request, f"Выбранные {queryset.count()} товары уже распроданы.")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('bulk-update-product-size/', self.bulk_update_product_size),
            path('bulk-update-product-color/', self.bulk_update_product_color),
        ]
        return new_urls + urls

    def bulk_update_product_size(self, request):
        if request.method == "POST":
            form = BulkUpdateProductSizeForm(request.POST)
            if form.is_valid():
                selected_product: Product = form.cleaned_data.get("product")
                selected_sizes: list[Size] = list(form.cleaned_data.get("sizes"))

                if not selected_product.size:
                    selected_product.size = selected_sizes.pop(0)
                    selected_product.save()
                else:
                    selected_sizes = list(filter(lambda s: s.size != selected_product.size.size, selected_sizes))

                product_data = model_to_dict(selected_product)
                season = product_data.pop("season_category")
                product_data["color"] = Color.objects.get(id=product_data["color"])
                product_data["type_category"] = TypeCategory.objects.get(id=product_data["type_category"])
                product_data.pop("id")
                product_data.pop("size")

                for size in selected_sizes:
                    new_product = Product(**product_data)
                    new_product.size = size
                    new_product.save()
                    new_product.season_category.set(season)

            messages.success(request, "Размеры успешно добавлены к товару!")
            url = reverse('admin:store_product_changelist')
            return HttpResponseRedirect(url)

        form = BulkUpdateProductSizeForm()
        data = {"form": form}
        return render(request, "admin/store/product/bulk-update-product-size.html", data)

    def bulk_update_product_color(self, request):
        if request.method == "POST":
            form = BulkUpdateProductColorForm(request.POST)
            if form.is_valid():
                pass

            messages.success(request, "Цвета успешно добавлены к товару!")
            url = reverse('admin:store_product_changelist')
            return HttpResponseRedirect(url)

        form = BulkUpdateProductColorForm()
        data = {"form": form}
        return render(request, "admin/store/product/bulk-update-product-color.html", data)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ("id", "product")


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    model = ProductSize
    list_display = ("product", "product_in_stock")
    search_fields = ("product",)

    def product_in_stock(self, obj):
        sizes = ", ".join([str(s.size) for s in obj.sizes.all()])
        return format_html("<b>{}</b>", sizes)
    product_in_stock.short_description = "Размеры в наличии"


@admin.register(SeasonCategory)
class SeasonCategoryAdmin(admin.ModelAdmin):
    model = SeasonCategory


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    model = Size


@admin.register(TypeCategory)
class TypeCategoryAdmin(admin.ModelAdmin):
    model = TypeCategory
    list_display = ("id", "name", "is_popular")
    search_fields = ("id", "name")


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    model = Color
    list_display = ("id", "color")
    search_fields = ("id", "color")
