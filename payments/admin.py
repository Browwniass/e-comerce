from django.contrib import admin
from payments.models import Payment
from payments.models.orders import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)