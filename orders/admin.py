from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'shipping_address', 'contact_number', 'snack', 'quantity', 'register_data', 'order_status']
    list_filter = ['register_data', 'order_status']

admin.site.register(Order, OrderAdmin)