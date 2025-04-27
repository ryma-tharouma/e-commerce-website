from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'customer_name', 'wilaya', 'express', 'created_at')
    search_fields = ('customer_name', 'order__id', 'shipment_id')
    list_filter = ('express', 'wilaya')