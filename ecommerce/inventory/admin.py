from django.contrib import admin
from .models import StockMovement, LowStockAlert

admin.site.register(StockMovement)
admin.site.register(LowStockAlert)

