from django.db import models
from cart.models import Order

class Shipment(models.Model):
    # order = models.OneToOneField(Order, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment")
    shipment_id = models.CharField(max_length=100, null=True, blank=True)  # ID from delivery API
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    source = models.IntegerField()
    wilaya = models.CharField(max_length=255)
    commune = models.IntegerField()
    express = models.BooleanField(default=False)
    note_to_driver = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="pending")  # or delivered/cancelled etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment for Order #{self.order.id}"
