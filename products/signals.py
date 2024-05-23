from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import convert_title_to_slug


@receiver(pre_save, sender="products.Product")
def check_price(instance, sender, **kwargs):
    if instance.discount_price < instance.price:
        raise ValidationError({"price": "Discount price must be less than price"})


@receiver(pre_save, sender="products.Product")
def check_stock(instance, sender, **kwargs):
    if instance.stock < 0:
        raise ValidationError({"stock": "Stock must be greater than or equal to zero"})


@receiver(pre_save, sender="products.Product")
def create_slug(instance, sender, **kwargs):
    instance.slug = convert_title_to_slug(instance)
