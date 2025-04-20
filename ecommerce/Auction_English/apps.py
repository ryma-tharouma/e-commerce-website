from django.apps import AppConfig


class English_AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Auction_English'
    def ready(self):
        import Auction_English.signal  # Ensure signals are loaded


   