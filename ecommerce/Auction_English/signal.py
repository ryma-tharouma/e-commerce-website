from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import EnglishAuctionItem
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from .views import send_invoice_email,generate_invoice

@receiver(post_save, sender=EnglishAuctionItem)
def check_auction_status(sender, instance, **kwargs):
    if (instance.end_time.replace(tzinfo=None) <= now().replace(tzinfo=None) and instance.winner is None):
        post_save.disconnect(check_auction_status, sender=EnglishAuctionItem)
        
        instance.determine_winner()
        
        print("sending an email ")
        send_invoice_email(instance,"nassabde227@gmail.com",generate_invoice(instance))
        
        instance.winner_notified = True
        instance.save()
        post_save.connect(check_auction_status, sender=EnglishAuctionItem)

