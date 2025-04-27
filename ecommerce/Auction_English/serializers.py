from rest_framework import serializers
from .models import EnglishAuctionItem, EnglishBid
# class AuctionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EnglishAuctionItem
#         fields = '__all__'

# class BidSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EnglishBid
#         fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    bidder_username = serializers.CharField(source='bidder.username', read_only=True)

    class Meta:
        model = EnglishBid
        fields = ['id', 'bidder', 'bidder_username', 'amount', 'timestamp']

class AuctionSerializer(serializers.ModelSerializer):
    english_auction_bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = EnglishAuctionItem
        fields = '__all__'