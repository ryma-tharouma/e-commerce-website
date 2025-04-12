from django import forms
from .models import StockMovement, low_stock_alert
from cart.models import Product

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'timestamp', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }


class LowStockAlertForm(forms.ModelForm):
    class Meta:
        model = LowStockAlert
        fields = ['product', 'reorder_level']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'stock']  # Fields to include in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter product price'}),
            'image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
        }