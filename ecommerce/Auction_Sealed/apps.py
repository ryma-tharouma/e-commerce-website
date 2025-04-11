from django.apps import AppConfig


class Sealed_AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Auction_Sealed'
    def ready(self):
        import Auction_Sealed.signal  # Ensure signals are loaded


   