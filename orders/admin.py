from django.contrib import admin

from .models import Order, OrderItem, Transaction

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Transaction)
