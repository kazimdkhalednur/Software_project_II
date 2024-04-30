from uuid import uuid4

from django.conf import settings
from django.db import models

USER = settings.AUTH_USER_MODEL


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ProductManager(models.Manager):
    def draft(self, **kwargs):
        return self.filter(status="draft", **kwargs)

    def published(self, **kwargs):
        return self.filter(status="published", **kwargs)

    def archived(self, **kwargs):
        return self.filter(status="archived", **kwargs)


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    id = models.UUIDField(primary_key=True, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    brand = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="products/thhumbnails/")
    description = models.TextField()
    discount_price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    price = models.DecimalField("Discount Price", max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    url = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.product.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
