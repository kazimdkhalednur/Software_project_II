from uuid import uuid4

from django.conf import settings
from django.db import models

from products.models import Product

from .utils import SSLCommerz

USER = settings.AUTH_USER_MODEL


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.title


class OrderManager(models.Manager):
    def get_user_orders(self, user):
        return self.filter(user=user)

    def pending(self, **kwargs):
        return self.filter(status=Order.OrderStatus.PENDING, **kwargs)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CANCELLED = "cancelled", "Cancelled"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        RECEIVED = "received", "Received"
        RETURNED = "returned", "Returned"
        REFUNDED = "refunded", "Refunded"

    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, null=True)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    status = models.CharField(
        max_length=15, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"

    def get_address(self):
        return self.address

    def get_address_2(self):
        return self.address_2

    def get_district(self):
        return self.district

    def get_postal_code(self):
        return self.postal_code


class TransactionManager(models.Manager):
    def pending(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.PENDING, **kwargs)

    def valid(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.VALID, **kwargs)

    def failed(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.FAILED, **kwargs)

    def cancelled(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.CANCELLED, **kwargs)

    def unattempted(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.UNATTEMPTED, **kwargs)

    def expired(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.EXPIRED, **kwargs)

    def refunded(self, **kwargs):
        return self.filter(status=Transaction.TransactionStatus.REFUNDED, **kwargs)


class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VALID = "VALID", "VALID"
        FAILED = "FAILED", "FAILED"
        CANCELLED = "CANCELLED", "CANCELLED"
        UNATTEMPTED = "UNATTEMPTED", "UNATTEMPTED"
        EXPIRED = "EXPIRED", "EXPIRED"
        REFUNDED = "REFUNDED", "REFUNDED"

    # before transaction complete
    id = models.UUIDField(primary_key=True, serialize=True, unique=True, editable=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=15,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    # after transaction
    sessionkey = models.CharField(max_length=50, blank=True, null=True)
    gateway_page_url = models.URLField(max_length=300, blank=True, null=True)
    tran_date = models.DateTimeField(blank=True, null=True)
    val_id = models.CharField(max_length=50, blank=True, null=True)
    bank_tran_id = models.CharField(max_length=80, blank=True, null=True)
    store_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    paid_at = models.DateTimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_refund = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)

    def check_valid_transaction(self):
        ssl_commerz = SSLCommerz()
        return ssl_commerz.validate_payment(self)
