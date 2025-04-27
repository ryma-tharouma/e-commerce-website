# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.utils.timezone import now
# from django.contrib.auth import get_user_model


# def get_admin_user():
#     admin_user=get_user_model().objects.filter(is_superuser=True).first()  # Get the first admin user
#     return admin_user.id if admin_user else None  


    
# class EnglishAuctionItem(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
    
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="english_auctions_product",default=1)
#     seller = models.ForeignKey(User, on_delete=models.CASCADE,default=get_admin_user)

#     starting_price = models.DecimalField(max_digits=10, decimal_places=2)
#     current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
#     start_time = models.DateTimeField(auto_now_add=True)
#     end_time = models.DateTimeField()
    
#     is_active = models.BooleanField(default=True)
    
#     current_winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_winner_english_auction")
#     winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_english_auction")
#     winner_notified=models.BooleanField(default=False)

#     def has_ended(self):
#         return self.end_time < now()
    
#     def determine_winner(self):
#         highest_bid = self.english_auction_bids.order_by('-amount').first()  # Get the highest bid

#         if highest_bid:
#             self.winner = highest_bid.bidder
#             self.is_active = False  # Mark the auction as ended
#             self.save()

#     def __str__(self):
#         return self.title
    
#     def save(self, *args, **kwargs):
#         from .tasks  import schedule_auction_notification
#         super().save(*args, **kwargs)  
#         # Schedule notification for exact end time
#         schedule_auction_notification(self)
        
    

# class EnglishBid(models.Model):
#     auction = models.ForeignKey(EnglishAuctionItem, on_delete=models.CASCADE,related_name="english_auction_bids")
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE,related_name="english_auction_bidder")
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
    
#     def clean(self):
#         """ Ensure user can bid before time ends and  only once per auction """
#         if self.auction.is_active==False :
#             raise ValidationError("Auction ended")
#         if (self.amount <= self.auction.starting_price):
#             raise ValidationError("Your bid must be higher than the starting price.")
#         if (self.amount <= self.auction.current_price ):
#             raise ValidationError("Your bid must be higher than the current price.")

#     def save(self, *args, **kwargs):
#         """ Validate before saving """
#         self.clean()  # Call validation
#         super().save(*args, **kwargs)  # Save the bid
#         self.auction.current_price = self.amount  # Update auction price
#         self.auction.current_winner = self.bidder  # Update current winner

#         self.auction.save()  # Save auction

#     class Meta:
#         ordering = ['-timestamp']
 
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()  
# User = settings.AUTH_USER_MODEL  
def get_admin_user():
    admin_user = User.objects.filter(is_superuser=True).first()
    return admin_user.id if admin_user else None

class EnglishAuctionItem(models.Model):
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='english_auction_items', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Set default seller to admin user using `get_admin_user` in the `save` method instead
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    current_winner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="current_winner_english_auction"
    )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_english_auction"
    )
    winner_notified = models.BooleanField(default=False)

    def has_ended(self):
        return self.end_time < now()

    def determine_winner(self):
        highest_bid = self.english_auction_bids.order_by('-amount').first()
        if highest_bid:
            self.winner = highest_bid.bidder
            self.is_active = False
            self.save()

    def save(self, *args, **kwargs):
        # Set default seller to admin user if not set
        if not self.seller:
            self.seller = get_admin_user()
        
        # You could also move the notification scheduling to a signal if needed
        from .tasks import schedule_auction_notification
        super().save(*args, **kwargs)
        schedule_auction_notification(self)

    def __str__(self):
        return self.title


class EnglishBid(models.Model):
    auction = models.ForeignKey(
        EnglishAuctionItem, on_delete=models.CASCADE, related_name="english_auction_bids"
    )
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="english_auction_bidder"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
# <<<<<<< HEAD
#         if not self.auction.is_active:
#             raise ValidationError("Auction has ended")
#         if self.amount <= self.auction.starting_price:
# =======
        """ Ensure user can bid before time ends and  only once per auction """
        if self.auction.is_active==False :
            raise ValidationError("Auction ended")
        if (self.amount <= self.auction.starting_price):
            
            raise ValidationError("Your bid must be higher than the starting price.")
        if self.amount <= self.auction.current_price:
            raise ValidationError("Your bid must be higher than the current price.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Update auction price and winner after each bid
        self.auction.current_price = self.amount
        self.auction.current_winner = self.bidder
        self.auction.save()

    class Meta:
        ordering = ['-timestamp']
