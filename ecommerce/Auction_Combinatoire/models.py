from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum
from pulp import LpMaximize, LpProblem, LpVariable
from django.utils.timezone import now
from Auction_English.models import get_admin_user


from pulp import LpMaximize, LpProblem, LpVariable, lpSum
from decimal import Decimal
# Combinatorial_
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

# Combinatorial_
class Combinatorial_Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name    
class CombinatorialAuction(models.Model):
    title = models.CharField(max_length=255, editable=True)
    description = models.TextField(default=" ")

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=get_admin_user)

    products = models.ManyToManyField(Combinatorial_Product, related_name="combinatorial_auctions")

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    
    Winner_list = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="Winner_list",blank=True)
  
    Winning_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def has_ended(self):
        return self.end_time <= now() # for some reason it doesnt work 
    
    def determine_winners(self):
        """Trouve les gagnants de l'enchère combinatoire en maximisant le gain total."""
        
        if self.end_time <= now() : # une verification en plus mais bon
 
            bids = list(CombinatorialBid.objects.filter(auction=self))  # Toutes les enchères proposées
            products = set(p for bid in bids for p in bid.products.all())  # Tous les produits concernés

            # Définition du problème d'optimisation
            prob = LpProblem("Maximize_Auction_Revenue", LpMaximize)

            # Variables binaires : 1 si une enchère est gagnante, 0 sinon
            bid_vars = {bid.id: LpVariable(f"bid_{bid.id}", 0, 1, cat="Binary") for bid in bids}

            # Fonction objective : maximiser le total des montants des offres sélectionnées
            prob += lpSum(float(bid.amount) * bid_vars[bid.id] for bid in bids), "Total_Revenue"

            # Contraintes : chaque produit ne peut être attribué qu'une seule fois
            for product in products:
                prob += lpSum(
                    bid_vars[bid.id] for bid in bids if product in bid.products.all()
                ) <= 1, f"Product_{product.id}_Constraint"

            # Résolution du problème d'optimisation
            prob.solve()

            # Extraction des gagnants
            winners = []
            for bid in bids:
                if bid_vars[bid.id].value() == 1:  # Si l'enchère est sélectionnée
                    winners.append(bid.user)
                    self.Winning_price = Decimal(self.Winning_price) + bid.amount

            # Mise à jour des gagnants

            if winners:
                self.Winning_price = sum(bid.amount for bid in bids if bid.user in winners)
                self.Winner_list.set(winners)  # On met à jour en une seule fois
            else:
                self.Winner_list.clear()
            
            self.save()
            return bids

 

from django import forms

class CombinatorialBid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(CombinatorialAuction, on_delete=models.CASCADE, related_name="combinatorial_bids")
    products = models.ManyToManyField(Combinatorial_Product,related_name="combinatorial_bids_product")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

            

    def save(self, *args, **kwargs):
        """ Validate before saving """
          # Call validation
        super().save(*args, **kwargs)  # Save the bid
        self.auction.save()  # Save auction
        
        
    def __str__(self):
        return f"{self.user.username} - {self.amount}$"

from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
# SIGNAL
@receiver(m2m_changed, sender=CombinatorialBid.products.through)
def validate_combinatorial_bid_products(sender, instance, action, **kwargs):
    if action == "pre_add":  # Trigger BEFORE products are added
        print("1")
        products_being_added = kwargs.get('pk_set')
        print("1")
        
        if not products_being_added:
            return
        auction = instance.auction
        user = instance.user

        if auction and user:
            # Fetch all other bids for this user in the same auction
            previous_bids = CombinatorialBid.objects.filter(
                auction=auction,
                user=user
            ).exclude(id=instance.id)

            # Get all products already used in other bids
            previous_products = set(
                p.id for bid in previous_bids for p in bid.products.all()
            )

            # Check overlap
            if previous_products & products_being_added:
                raise ValidationError(
                    "You cannot bid on a product that you already bid on in this auction."
                )