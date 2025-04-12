from django.contrib import admin
from .models import StockMovement, LowStockAlert, ProductListing

admin.site.register(StockMovement)
admin.site.register(LowStockAlert)
admin.site.register(ProductListing)
