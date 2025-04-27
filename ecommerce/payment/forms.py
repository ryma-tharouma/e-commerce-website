from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["client", "client_email", "invoice_number", "amount", "discount", "mode", "comment"]
