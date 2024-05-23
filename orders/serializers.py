from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Order, OrderItem


class MessageSerializer(serializers.Serializer):
    msg = serializers.CharField()


class BuyerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["address", "address_2", "district", "postal_code"]


class CheckOutPriceDetailSerializer(serializers.Serializer):
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentSerializer(serializers.Serializer):
    gateway_page_url = serializers.URLField()


class BuyerOrderItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["title", "quantity", "unit_price", "total_price"]

    @extend_schema_field(serializers.CharField)
    def get_title(self, order_item):
        return order_item.product.title

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_unit_price(self, order_item):
        return order_item.product.price


class BuyerOrderSerializer(serializers.ModelSerializer):
    paid_at = serializers.SerializerMethodField()
    items = BuyerOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items", "status", "paid_at"]

    @extend_schema_field(serializers.DateTimeField)
    def get_paid_at(self, order):
        return order.transactions.filter(status="VALID")[0].paid_at
