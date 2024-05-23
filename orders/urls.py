from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("ipn/", views.OrderInstantPaymentNotificationView.as_view(), name="ipn"),
    path("my-orders/", views.MyOrderListView.as_view(), name="my_orders"),
]
