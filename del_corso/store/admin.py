import logging

from django.contrib import admin, messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.html import format_html

from del_corso.logging import setup_logging
from store.forms import BulkUpdateProductSizeForm, BulkRemoveSeasonCategoryForm, ColorForm
from store.inlines import ProductImage, ProductImageAdminInline
from store.models import Product, SeasonCategory, Size, TypeCategory, Color
from store.models.product import ProductSize


setup_logging()
logger = logging.getLogger(__name__)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = (
        "id",
        "vendor_code",
        "price",
        "color",
        "season_categories",
        "type_category",
        "in_stock",
        "size",
        "quantity"
    )
    search_fields = ("id", "name", "price", "vendor_code")
    actions = ("set_in_stock", "set_out_of_stock", "sell_one_product", "duplicate_products_by_color")
    inlines = (ProductImageAdminInline, )
    action_form = ColorForm

    def season_categories(self, obj: Product):
        return ", ".join([str(category) for category in obj.season_category.all()])

    season_categories.short_description = "Сезон"

    @admin.action(description="Добавить 1 товар")
    def set_in_stock(self, request, queryset: list[Product]) -> None:
        for product in queryset:
            product.in_stock = True
            product.quantity = 1
            product.save()
        logger.info(f"Set `in_stock` status for {len(queryset)} Product objects")
        self.message_user(request, f"Выбранные {queryset.count()} товары теперь в наличии.")

    @admin.action(description="Распродано")
    def set_out_of_stock(self, request, queryset: list[Product]) -> None:
        for product in queryset:
            product.in_stock = False
            product.quantity = 0
            product.save()
        logger.info(f"Set `out_of_stock` status for {len(queryset)} Product objects")
        self.message_user(request, f"Выбранные {queryset.count()} товары уже распроданы.")

    @admin.action(description="Продать 1 Товар")
    def sell_one_product(self, request, queryset: list[Product]):
        for product in queryset:
            if product.quantity > 0:
                product.quantity -= 1
                product.save()
        logger.info(f"Sold 1 pair for {len(queryset)} Product objects")
        self.message_user(request, "Количество выбранных товаров уменьшилось на 1 единицу для каждого товара")

    @admin.action(description="Дублировать товар")
    def duplicate_products_by_color(self, request, queryset: list[Product]):
        colors: list[str] = request.POST.getlist("color", None)
        if not colors:
            logger.info(f"Got invalid POST body while duplicating products: {request.POST}. Aborting...")
            self.message_user(request, "Выберите верное дейстие!")
        for color in colors:
            for product in queryset:
                product_data = model_to_dict(product)
                product_data.pop("color")
                product_data.pop("id")
                season = product_data.pop("season_category")
                product_data["type_category"] = TypeCategory.objects.get(id=product_data["type_category"])
                product_data["size"] = Size.objects.get(pk=int(product_data["size"]))
                new_color = Color.objects.get(pk=int(color))
                with transaction.atomic():
                    new_product = Product.objects.create(**product_data, color=new_color)
                    new_product.season_category.set(season)
                    logger.info(
                        f"New product {product.name} ({product.id}) created successfully with new color - {new_color.color}"
                    )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('bulk-update-product-size/', self.bulk_update_product_size),
            path('bulk-remove-seasons/', self.bulk_remove_seasons)
        ]
        return new_urls + urls

    def bulk_remove_seasons(self, request):
        if request.method == "POST":
            form = BulkRemoveSeasonCategoryForm(request.POST)
            if form.is_valid():
                seasons_to_remove: list[SeasonCategory] = form.cleaned_data.get("season_categories")
                for season in seasons_to_remove:
                    products = Product.objects.filter(season_category=season)
                    for product in products:
                        if not len(product.season_category.all()) > 1:
                            product.quantity = 0
                            product.in_stock = False
                            product.save()
                logger.info(f"{seasons_to_remove} are removed successfully!")
                messages.success(request, "Сезоны успешно отключены!")

                url = reverse('admin:store_product_changelist')
                return HttpResponseRedirect(url)
            else:
                logger.error(f"Failed to remove the seasons. The form is invalid: {form.errors}")
                messages.error(request, "Произошла ошибка. Пожалуйста, заполните данные еще раз")

        form = BulkRemoveSeasonCategoryForm()
        data = {"form": form}
        return render(request, "admin/store/product/bulk-remove-seasons.html", data)

    def bulk_update_product_size(self, request):
        if request.method == "POST":
            logger.info("Creating Product objects with different sizes...")
            form = BulkUpdateProductSizeForm(request.POST)
            if form.is_valid():
                selected_product: Product = form.cleaned_data.get("product")
                selected_sizes: list[Size] = list(form.cleaned_data.get("sizes"))
                size_quantities: dict[int] = form.cleaned_data.get("size_quantities")

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

                for size, quantity in zip(selected_sizes, size_quantities.values()):
                    with transaction.atomic():
                        new_product = Product(**product_data)
                        new_product.size = size
                        new_product.quantity = quantity
                        new_product.save()
                        new_product.season_category.set(season)

                logger.info(f"{selected_sizes} updated successfully!")
                messages.success(request, "Размеры успешно добавлены к товару!")
            else:
                logger.error(f"Failed to create new Product objects. The form is invalid: {form.errors}")
                messages.error(request, "Произошла ошибка. Пожалуйста, заполните данные еще раз")
            url = reverse('admin:store_product_changelist')
            return HttpResponseRedirect(url)

        form = BulkUpdateProductSizeForm()
        data = {"form": form}
        return render(request, "admin/store/product/bulk-update-product-size.html", data)

    def delete_model(self, request, obj):
        logger.info(
            f"Deleting Product object ({obj.id} - {obj.vendor_code})...\n Deleting related ProductSize object..."
        )
        obj.delete_related_productsize_size(vendor_code=obj.vendor_code, size=obj.size)
        obj.delete()
        logger.info(f"Product object ({obj.id} - {obj.vendor_code}) deleted successfully!")

    def delete_queryset(self, request, queryset):
        logger.info(f"Deleting {len(queryset)} Product objects...\n Deleting related ProductSize objects...")
        for product in queryset:
            product.delete_related_productsize_size(vendor_code=product.vendor_code, size=product.size)
            product.delete()
        logger.info(f"{len(queryset)} Product objects deleted successfully!")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    model = ProductImage
    list_display = ("id", "product")
    search_fields = ("product__vendor_code", )


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    model = ProductSize
    list_display = ("vendor_code", "sizes_available")
    search_fields = ("vendor_code",)

    def sizes_available(self, obj):
        sizes = ", ".join([str(s.size) for s in obj.sizes.all()])
        return format_html("<b>{}</b>", sizes)
    sizes_available.short_description = "Размеры в наличии"


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
