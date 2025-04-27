from django.contrib import admin
from .models import StockMovement, LowStockAlert
from django.utils.html import format_html
from django.db.models import Sum, Case, When, Value, IntegerField, F

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'timestamp', 'current_stock', 'remarks')
    list_filter = ('movement_type', 'timestamp', 'product')
    search_fields = ('product__name', 'remarks')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    
    def current_stock(self, obj):
        # Calculate current stock by summing IN movements and subtracting OUT movements
        total = StockMovement.objects.filter(product=obj.product).aggregate(
            total=Sum(
                Case(
                    When(movement_type='IN', then='quantity'),
                    When(movement_type='OUT', then=-1 * F('quantity')),
                    When(movement_type='ADJ', then='quantity'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        )['total'] or 0
        return total

@admin.register(LowStockAlert)
class LowStockAlertAdmin(admin.ModelAdmin):
    list_display = ('product', 'reorder_level', 'current_stock', 'status')
    list_filter = ('reorder_level',)
    search_fields = ('product__name',)
    
    def current_stock(self, obj):
        # Calculate current stock by summing IN movements and subtracting OUT movements
        total = StockMovement.objects.filter(product=obj.product).aggregate(
            total=Sum(
                Case(
                    When(movement_type='IN', then='quantity'),
                    When(movement_type='OUT', then=-1 * F('quantity')),
                    When(movement_type='ADJ', then='quantity'),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        )['total'] or 0
        return total
    
    def status(self, obj):
        current_stock = self.current_stock(obj)
        if current_stock <= obj.reorder_level:
            return format_html(
                '<span style="color: red; font-weight: bold;">LOW STOCK - Reorder Now</span>'
            )
        return format_html(
            '<span style="color: green;">In Stock</span>'
        )

