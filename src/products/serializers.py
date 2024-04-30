from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Product, ProductImage


class ProductsSerializer(ModelSerializer):
    category = serializers.SerializerMethodField

    class Meta:
        model = Product
        fields = (
            "title",
            "thumbnail",
            "discount_price",
            "price",
            "sold",
            "rating",
            "category",
        )

    def get_category(self, product):
        return product.category.title


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("url",)


class ProductSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ("id", "created_at", "updated_at", "status")
