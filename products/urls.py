from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("cart/", views.CartListView.as_view(), name="cart_list"),
    path("cart/create/", views.CartCreateView.as_view(), name="cart_create"),
    path("<str:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
]
