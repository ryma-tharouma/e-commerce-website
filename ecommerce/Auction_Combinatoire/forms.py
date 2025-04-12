# forms.py

from django import forms
from .models import CombinatorialBid

class CombinatorialBidForm(forms.ModelForm):
    class Meta:
        model = CombinatorialBid
        fields = "__all__"
    
    def clean(self):
        cleaned_data = super().clean()
        auction = cleaned_data.get("auction")
        user = cleaned_data.get("user")
        products = cleaned_data.get("products")

        if auction and user and products:
            # Check if user already bid on these products
            for product in products:
                existing_bids = CombinatorialBid.objects.filter(
                    auction=auction, user=user, products=product
                )
                if existing_bids.exists():
                    raise forms.ValidationError(
                        f"You cannot bid on the product '{product.name}' that you already bid on in this auction."
                    )

        return cleaned_data
