from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('FURNITURE_DECO', 'Furniture & Decor'),
        ('JEWELRY', 'Jewelry'),
        ('FINE_ART', 'Fine Art'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='FURNITURE_DECO')

    def __str__(self):
        return self.name

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Commande {self.id} - {self.total_price}€"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.quantity * self.product.price
    

class CartItem(models.Model):
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

