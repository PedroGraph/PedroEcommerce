from django.contrib import admin
from .models import Orders, OrderDetails, Products, Customers, Cart


admin.site.register(Orders)
admin.site.register(OrderDetails)
admin.site.register(Products)
admin.site.register(Customers)
admin.site.register(Cart)
# Register your models here.
