from decimal import Decimal

from django.db import transaction as database_transaction
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response

from products.models import Cart

from .models import Order, OrderItem, Transaction
from .serializers import (
    BuyerAddressSerializer,
    BuyerOrderSerializer,
    CheckOutPriceDetailSerializer,
    MessageSerializer,
    PaymentSerializer,
)
from .utils import SSLCommerz


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerAddressSerializer

    @extend_schema(
        responses={200: CheckOutPriceDetailSerializer},
    )
    def get(self, request, *args, **kwargs):
        cart_total = Cart.objects.get(user=request.user).get_total()
        delivery_fee = 5
        data = {
            "cart_total": cart_total,
            "delivery_fee": delivery_fee,
            "total": cart_total + delivery_fee,
        }
        serializer = CheckOutPriceDetailSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: PaymentSerializer},
    )
    def post(self, request, *args, **kwargs):
        with database_transaction.atomic():
            order = BuyerAddressSerializer(data=request.data)
            order.is_valid(raise_exception=True)
            order = Order.objects.create(**order.validated_data, user=request.user)

            order_item = []
            for cart in (
                Cart.objects.select_related("product")
                .only(
                    "quantity",
                    "product__id",
                    "product__price",
                )
                .select_for_update()
                .filter(user=self.request.user)
            ):
                order_item.append(
                    OrderItem(
                        product=cart.product,
                        quantity=cart.quantity,
                        total_price=cart.product.price * cart.quantity,
                    )
                )
            order_items = OrderItem.objects.bulk_create(order_item)
            order.items.set(order_items)

            transaction = Transaction.objects.create(
                order=order,
                amount=order.items.aggregate(total=Sum(F("total_price")))["total"]
                + Decimal(5),
            )

            payment = SSLCommerz()
            url = self.request.build_absolute_uri(reverse("orders:ipn"))
            payment.set_urls(
                success_url=url,
                fail_url=url,
                cancel_url=url,
                ipn_url=url,
            )

            response_data = payment.init_payment(transaction, order, self.request.user)

            if response_data["status"] == "FAILED":
                return Response(
                    response_data["failedreason"], status=status.HTTP_400_BAD_REQUEST
                )
            elif response_data["status"] == "SUCCESS":
                transaction.sessionkey = response_data["sessionkey"]
                transaction.gateway_page_url = response_data["GatewayPageURL"]
                transaction.save()

            Cart.objects.filter(user=self.request.user).delete()

        data = {
            "gateway_page_url": response_data["GatewayPageURL"],
        }
        serializer = PaymentSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class OrderInstantPaymentNotificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        payment_data = request.POST

        if payment_data["status"] == "VALID":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.tran_date = payment_data["tran_date"]
            transaction.status = payment_data["status"]
            transaction.val_id = payment_data["val_id"]
            transaction.store_amount = payment_data["store_amount"]
            transaction.bank_tran_id = payment_data["bank_tran_id"]
            transaction.paid_at = timezone.now()
            transaction.is_paid = True
            transaction.save(
                update_fields=[
                    "tran_date",
                    "status",
                    "val_id",
                    "store_amount",
                    "bank_tran_id",
                    "is_paid",
                    "paid_at",
                ]
            )
            transaction.order.status = Order.OrderStatus.PAID
            transaction.order.save(update_fields=["status"])
            return Response(
                {"msg": "Order has been placed successfully."},
                status=status.HTTP_200_OK,
            )

        elif payment_data["status"] == "FAILED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save(update_fields=["status"])
            return Response(
                {"msg": "Order has been failed."}, status=status.HTTP_400_BAD_REQUEST
            )

        elif payment_data["status"] == "CANCELLED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save(update_fields=["status"])
            return Response(
                {"msg": "Order has been canceled by you."}, status=status.HTTP_200_OK
            )

        elif payment_data["status"] == "UNATTEMPTED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save(update_fields=["status"])
            return Response(
                {"msg": "Order has been unattempted."}, status=status.HTTP_200_OK
            )

        elif payment_data["status"] == "EXPIRED":
            transaction = get_object_or_404(Transaction, id=payment_data["tran_id"])
            transaction.status = payment_data["status"]
            transaction.save(update_fields=["status"])
            return Response(
                {"msg": "Order has been expired."}, status=status.HTTP_400_BAD_REQUEST
            )


class MyOrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status="pending")
