from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import SealedAuctionItem
from django.core.mail import send_mail
from Auction_English.views import generate_invoice,send_invoice_email

@receiver(post_save, sender=SealedAuctionItem)
def check_auction_status(sender, instance, **kwargs):
    post_save.disconnect(check_auction_status, sender=SealedAuctionItem)

    if instance.end_time.replace(tzinfo=None) <= now().replace(tzinfo=None) and instance.winner==None:
        instance.determine_winner()
        if instance.winner:
            print("sending an email ")
            print(instance.winner)
            # send_invoice_email(instance,instance.winner.email,generate_invoice(instance))
            send_invoice_email(instance,"nassabde227@gmail.com",generate_invoice(instance))
            print("sent ")
            
            instance.winner_notified = True
            instance.save()

    post_save.connect(check_auction_status, sender=SealedAuctionItem)
