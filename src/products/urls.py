from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view()),
    path("cart/", views.CartListView.as_view()),
    path("cart/create/", views.CartCreateView.as_view()),
    path("<str:slug>/", views.ProductDetailView.as_view()),
]
