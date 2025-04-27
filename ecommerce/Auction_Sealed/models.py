from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Auction_English.models import get_admin_user

# from django.utils.timezone import now

class SealedAuctionItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    # product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="sealed_auctions_product",default=1)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_admin_user)
    
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    # current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    
    # seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sealed_auction_seller")
    
    is_active = models.BooleanField(default=True)
    
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_sealed_auctions")
    Winning_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # winning_bid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_sealed_auctions")

    def determine_winner(self):
        """ Determines the winner for a first-price sealed-bid auction. """
     # if self.is_active and self.end_time <= now():
        highest_bid = self.sealed_auction_bids.order_by('-amount').first()  
        if highest_bid:
            self.winner = highest_bid.bidder  # Highest bidder wins
            self.Winning_price = highest_bid.amount  # Highest bidder wins
             

        self.is_active = False  # Mark auction as closed
        self.save()

    def __str__(self):
        return self.title
    

class SealedBid(models.Model):
    auction = models.ForeignKey(SealedAuctionItem, on_delete=models.CASCADE,related_name="sealed_auction_bids")
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="sealed_auction_bidder")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        """ Ensure user can bid before time ends and  only once per auction """
        if self.auction.is_active==False :
            raise ValidationError("Auction ended")
        
        if SealedBid.objects.filter(auction=self.auction, bidder=self.bidder).exists():
            raise ValidationError("You have already placed a bid for this auction.")
        
        if (self.amount <= self.auction.starting_price):
            raise ValidationError("Your bid must be higher than the starting price.")
        
    

    def save(self, *args, **kwargs):
        """ Validate before saving """

        self.clean()  # Call validation
        super().save(*args, **kwargs)  # Save the bid

        self.auction.save()  # Save auction

    class Meta:
        ordering = ['-timestamp']
 

