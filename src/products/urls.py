from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view()),
    path("<str:slug>/", views.ProductDetailView.as_view()),
]
