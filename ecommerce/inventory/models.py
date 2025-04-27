from django.db import models
from django.utils.timezone import now
from cart.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    def save(self, *args, **kwargs):
        # Calculate the change in stock based on movement type
        if self.movement_type == 'IN':
            change = self.quantity
        elif self.movement_type == 'OUT':
            change = -self.quantity
        else:  # ADJ
            # For adjustment, we set the stock to the exact quantity
            self.product.stock = self.quantity
            self.product.save()
            super().save(*args, **kwargs)
            return

        # Update the product's stock
        self.product.stock += change
        self.product.save()

        # Save the stock movement
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # When deleting a movement, we need to reverse its effect
        if self.movement_type == 'IN':
            change = -self.quantity
        elif self.movement_type == 'OUT':
            change = self.quantity
        else:  # ADJ
            # For adjustment, we can't reliably reverse it, so we'll just delete
            super().delete(*args, **kwargs)
            return

        # Update the product's stock
        self.product.stock += change
        self.product.save()

        # Delete the movement
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']


class LowStockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='low_stock_alerts')
    reorder_level = models.PositiveIntegerField(default=5)  # Default reorder level of 5
    created_at = models.DateTimeField(default=now)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Low Stock Alert for {self.product.name}: Reorder when below {self.reorder_level}"

    class Meta:
        ordering = ['-created_at']


@receiver(post_save, sender=StockMovement)
def check_stock_levels(sender, instance, **kwargs):
    """
    Signal to check stock levels after any stock movement and create/resolve alerts
    """
    product = instance.product
    reorder_level = 5  # Default reorder level
    
    # Check if stock is below reorder level
    if product.stock <= reorder_level:
        # Create alert if one doesn't exist
        LowStockAlert.objects.get_or_create(
            product=product,
            resolved=False,
            defaults={'reorder_level': reorder_level}
        )
    else:
        # If stock is above reorder level, resolve any existing alerts
        LowStockAlert.objects.filter(
            product=product,
            resolved=False
        ).update(
            resolved=True,
            resolved_at=now()
        )