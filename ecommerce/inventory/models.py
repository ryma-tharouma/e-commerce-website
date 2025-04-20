from django.db import models
from django.utils.timezone import now
from cart.models import Product


class StockMovement(models.Model):
    STOCK_MOVEMENT_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=3, choices=STOCK_MOVEMENT_TYPES)
    quantity = models.IntegerField()  # Positive for 'IN', negative for 'OUT'
    timestamp = models.DateTimeField(default=now)
    remarks = models.TextField(null=True, blank=True)  # Optional notes about the movement

    def __str__(self):
        return f"{self.get_movement_type_display()} {abs(self.quantity)} of {self.product.name} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class LowStockAlert(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='low_stock_alert')
    reorder_level = models.PositiveIntegerField(default=10)  # Threshold for triggering alerts

    def __str__(self):
        return f"Low Stock Alert for {self.product.name}: Reorder when below {self.reorder_level}"