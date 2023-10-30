from sys import stdout

from discounts.models import Discount
from store.enums.material_enum import LiningMaterialType
from store.models import Product, Size, Color, TypeCategory, ProductSize


class PopulateDbBuilder:
    def __init__(self, dicsount_vendor_code: str = "0000-0000"):
        self.create_products(discount_vendor_code=dicsount_vendor_code)
        self.create_order()
        self.create_discount(dicsount_vendor_code=dicsount_vendor_code)

    def create_products(self, discount_vendor_code: str):
        sizes = Size.objects.all()

        product_1 = Product(
            name="Белые кеды",
            price=150,
            vendor_code=discount_vendor_code,
            lining_material=LiningMaterialType.BAIZE,
            heel_height=5,
            sole_height=5,
            guarantee_period=60,
            importer="БелОбувь",
            size=sizes[0],
            color=Color.objects.get(color="Белый"),
            type_category=TypeCategory.objects.get(name="Кеды")
        )
        product_size_1 = ProductSize(
            vendor_code=discount_vendor_code
        )

        product_2 = Product(
            name="Черныe лоферы",
            price=340,
            vendor_code="1111-1111",
            lining_material=LiningMaterialType.BAIZE,
            heel_height=3,
            sole_height=3,
            guarantee_period=60,
            importer="БелОбувь",
            size=sizes[1],
            color=Color.objects.get(color="Черный"),
            type_category=TypeCategory.objects.get(name="Лоферы")
        )
        product_size_2 = ProductSize(
            vendor_code="1111-1111"
        )

        product_3 = Product(
            name="Красные ботинки",
            price=400,
            vendor_code="2222-2222",
            lining_material=LiningMaterialType.BAIZE,
            heel_height=10,
            sole_height=10,
            guarantee_period=60,
            importer="БелОбувь",
            size=sizes[2],
            color=Color.objects.get(color="Красный"),
            type_category=TypeCategory.objects.get(name="Ботинки")
        )
        product_size_3 = ProductSize(
            vendor_code="2222-2222"
        )

        Product.objects.bulk_create([
            product_1,
            product_2,
            product_3
        ])
        stdout.write("Products have been created successfully!\n")

        ProductSize.objects.bulk_create([
            product_size_1,
            product_size_2,
            product_size_3
        ])
        product_size_1.products.add(product_1)
        product_size_1.sizes.add(sizes[0])

        product_size_2.products.add(product_2)
        product_size_2.sizes.add(sizes[1])

        product_size_3.products.add(product_3)
        product_size_3.sizes.add(sizes[2])

        stdout.write("ProductSize objects have been created successfully!\n")

    def create_order(self):
        pass

    def create_discount(self, dicsount_vendor_code: str):
        Discount.objects.create(
            name=dicsount_vendor_code,
            discount_price=59.9,
            start_date="2023-07-07",
            end_date="2025-07-07"
        )
        stdout.write("Discount has been created successfully!\n")
