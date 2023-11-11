import logging

from django.apps import apps
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from base_models import BaseModel
from store.models.category import (
    SeasonCategory,
    TypeCategory,
    Size,
    Color
)
from store.enums.material_enum import (
    UpperMaterialType,
    LiningMaterialType,
    CompletenessType,
    TrueToSizeType
)

from del_corso import setup_logging
from del_corso.config import general_config

setup_logging()
logger = logging.getLogger(__name__)


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    vendor_code = models.CharField(max_length=100, verbose_name="Артикул")
    new_collection = models.BooleanField(default=True, verbose_name="Новая коллекция")

    upper_material = models.CharField(
        max_length=50,
        choices=UpperMaterialType.choices,
        verbose_name="Материал верха",
        default=UpperMaterialType.GENUINE_LEATHER,
        null=True,
    )
    lining_material = models.CharField(
        max_length=50,
        choices=LiningMaterialType.choices,
        verbose_name="Материал подкладки",
        null=True,
    )
    heel_height = models.FloatField(null=True,
                                    validators=[
                                        MinValueValidator(0,
                                                          message="Высота каблука должна быть положительным значением")
                                    ],
                                    verbose_name="Высота каблука")
    sole_height = models.FloatField(null=True,
                                    validators=[
                                        MinValueValidator(0,
                                                          message="Высота подошвы должна быть положительным значением")
                                    ],
                                    verbose_name="Высота подошвы")
    completeness = models.CharField(
        max_length=50,
        choices=CompletenessType.choices,
        verbose_name="Полнота",
        default=CompletenessType.AVERAGE,
        null=True,
    )
    true_to_size = models.CharField(
        max_length=50,
        choices=TrueToSizeType.choices,
        verbose_name="Соответствие размера",
        default=TrueToSizeType.EXACT_SIZE,
        null=True,
    )
    country_of_origin = models.CharField(
        max_length=50,
        verbose_name="Страна производства",
        default="Турция",
        null=True
    )
    guarantee_period = models.PositiveSmallIntegerField(verbose_name="Гарантийный срок (дней)", null=True)
    importer = models.CharField(max_length=200, verbose_name="Импортер", null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Размер", blank=True, null=True)
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество", default=2)

    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Цвет")
    season_category = models.ManyToManyField(SeasonCategory, verbose_name="Сезон")
    type_category = models.ForeignKey(TypeCategory, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.vendor_code} - {self.price}р - {self.color} ({self.size})"

    def save(self, *args, **kwargs):
        curr_quantity = self.quantity < 1
        self.in_stock = not curr_quantity

        super().save(*args, **kwargs)
        logger.info(
            f"Product object ({self.vendor_code} - {self.size.size}) updated. The product currently in stock: {self.in_stock}"
        )

        logger.info("Updating ProductSize related object...")
        product_size, created = ProductSize.objects.get_or_create(
            vendor_code=self.vendor_code,
            defaults={'vendor_code': self.vendor_code},
        )
        product_size.products.add(self)

        if self.size and (self.in_stock or not curr_quantity):
            product_size.sizes.add(self.size.id)

        if (not self.in_stock or curr_quantity) and self.size:
            product_size.sizes.remove(self.size)
        product_size.save()
        logger.info(
            f"ProductSize object ({product_size.id}) updated successfully! The sizes are {product_size.sizes.all()}"
        )

        if not product_size.sizes.all():
            product_size.delete()
            logger.info(f"ProductSize ({product_size.id}) object deleted due to lack of sizes")

    def get_current_price(self) -> float | models.DecimalField | int:
        """Get product's current price considering a discount"""

        product_discount_model = apps.get_model('discounts', 'ProductDiscount')
        active_discount = product_discount_model.objects.filter(
            product=self,
            discount__start_date__lte=timezone.now().date(),
            discount__end_date__gte=timezone.now().date()
        ).first()

        if active_discount:
            return active_discount.discount.discount_price
        return self.price

    @staticmethod
    def delete_related_productsize_size(vendor_code: str, size: Size) -> None:
        logger.info(f"Removing size ({size}) from ProductSize object with vendor code `{vendor_code}`")
        product_size = ProductSize.objects.get(vendor_code=vendor_code)
        product_size.sizes.remove(size)
        logger.info(f"Size {size} removed successfully!")

    class Meta:
        app_label = "store"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductSize(BaseModel):
    vendor_code = models.CharField(max_length=100, verbose_name="Артикул", default="-")
    products = models.ManyToManyField(Product, verbose_name="Товары", null=True, blank=True)
    sizes = models.ManyToManyField(Size, verbose_name="Размеры в наличии")

    def __str__(self):
        return f"{self.vendor_code}"

    class Meta:
        app_label = "store"
        verbose_name = "Размер товара"
        verbose_name_plural = "Размеры товаров"


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    image = models.FileField(
        upload_to=general_config.TARGET_IMAGE_DIR,
        verbose_name="Изображение",
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg"))],
    )
    primary = models.BooleanField(default=False, verbose_name="Основная фотография")

    def __str__(self):
        return f"{self.product.vendor_code} - {self.product.price}"

    class Meta:
        app_label = "store"
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
