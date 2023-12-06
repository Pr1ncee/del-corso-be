from django.db.models.signals import pre_delete
from django.dispatch import receiver

from store.models import Product, ProductImage


@receiver(pre_delete, sender=Product)
def delete_product_images(sender, instance, **kwargs):
    product_images = ProductImage.objects.filter(product=instance)
    for product_image in product_images:
        product_image.delete()
