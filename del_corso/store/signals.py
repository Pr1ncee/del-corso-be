from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from store.models import Product, ProductSize


@receiver(pre_delete, sender=Product)
def update_product_size_on_product_delete(sender, instance, **kwargs):
    product = instance

    if product.size:
        try:
            print('sithosnithnisthoinstoh')
            product_size = ProductSize.objects.get(product=product)
            product_size.sizes.remove(product.size)
        except ObjectDoesNotExist:
            print('the object does not exist')
            pass
