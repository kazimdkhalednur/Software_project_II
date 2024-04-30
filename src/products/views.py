from rest_framework.generics import ListAPIView, RetrieveAPIView

from . import serializers
from .models import Product


class ProductListView(ListAPIView):
    serializer_class = serializers.ProductsSerializer

    def get_queryset(self):
        return (
            Product.objects.select_related("category")
            .only(
                "title",
                "thumbnail",
                "discount_price",
                "price",
                "sold",
                "rating",
                "category__title",
            )
            .filter(status="published")
        )


class ProductDetailView(RetrieveAPIView):
    lookup_field = "slug"
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return (
            Product.objects.prefetch_related("images")
            .select_related("category")
            .filter(status="published")
        )
