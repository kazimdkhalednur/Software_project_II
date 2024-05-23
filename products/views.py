from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import Response

from . import serializers
from .models import Cart, Product


class ProductListView(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Product.objects.select_related("category")
            .only(
                "title",
                "slug",
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
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Product.objects.prefetch_related("images")
            .select_related("category")
            .filter(status="published")
        )


@extend_schema(
    responses={
        201: OpenApiResponse(
            response=serializers.CartSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={"message": "Cart added successfully"},
                    response_only=True,
                    status_codes=["201"],
                ),
            ],
        ),
    }
)
class CartCreateView(CreateAPIView):
    serializer_class = serializers.CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"message": "Cart added successfully"}, status=status.HTTP_201_CREATED
        )


class CartListView(ListAPIView):
    serializer_class = serializers.CartListSerializer

    def get_queryset(self):
        return (
            Cart.objects.select_related("product")
            .only(
                "product__title",
                "product__thumbnail",
                "product__discount_price",
                "product__price",
                "quantity",
            )
            .filter(user=self.request.user)
        )
