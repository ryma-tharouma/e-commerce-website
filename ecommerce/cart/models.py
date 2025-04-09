from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, null=True, blank=True, default=None)
    stock = models.PositiveIntegerField(default=0)

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
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # Chaque panier est lié à un utilisateur
    session_id = models.CharField(max_length=255, null=True, blank=True)  # ID unique de session
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Produit ajouté au panier
    quantity = models.PositiveIntegerField(default=1)  # Quantité d'articles

    def __str__(self):
        return f"{self.quantity} x {self.product.name} "

