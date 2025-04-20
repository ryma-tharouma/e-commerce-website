from django.contrib import admin
from .models import Product, CartItem, Order, OrderItem  # Ajoute tes modèles ici

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description')

# Register your models here.

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
