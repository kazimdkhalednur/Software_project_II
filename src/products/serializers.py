from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Cart, Product, ProductImage


class ProductListSerializer(ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "title",
            "slug",
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


class CartSerializer(ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="slug", queryset=Product.objects.published()
    )

    class Meta:
        model = Cart
        fields = ["product", "quantity"]

    def save(self, **kwargs):
        user = kwargs["user"]
        product = self.validated_data["product"]
        return Cart.objects.update_or_create(
            user=user, product=product, defaults=self.validated_data
        )


class CartProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "thumbnail",
            "discount_price",
            "price",
        )


class CartListSerializer(ModelSerializer):
    product = CartProductSerializer()

    class Meta:
        model = Cart
        fields = ["id", "product", "quantity"]
