from django.contrib import admin

from .models import Cart, Category, Product, ProductImage

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Cart)