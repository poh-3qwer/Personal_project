from django.contrib import admin
from core_order.models import Order, OrderItem


admin.site.register(OrderItem)
admin.site.register(Order)