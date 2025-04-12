from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import CombinatorialAuction

@receiver(post_save, sender=CombinatorialAuction)
def check_auction_status(sender, instance, **kwargs):
    if instance.end_time.replace(tzinfo=None) <= now().replace(tzinfo=None) and instance.Winner_list==None :
        
        # Désactiver le signal
        post_save.disconnect(check_auction_status, sender=CombinatorialAuction)
        
        instance.determine_winners()

        # Réactiver le signal après l'exécution
        post_save.connect(check_auction_status, sender=CombinatorialAuction)

