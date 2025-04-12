from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EnglishAuctionItem, EnglishBid

@admin.register(EnglishAuctionItem)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_price', 'current_price', 'end_time', 'is_active', 'seller','current_winner', 'winner')
    list_filter = ('is_active', 'end_time')
    search_fields = ('title', 'description')

    def get_winner(self, obj):
        return obj.winner.username if obj.winner else "No Winner"
    get_winner.short_description = "Winner"
    
    
    def get_seller(self, obj):
        return obj.product.seller.username if obj.product else "No product"
    get_seller.short_description = "Seller"


@admin.register(EnglishBid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('auction__title', 'bidder__username')
