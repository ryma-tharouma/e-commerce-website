from rest_framework import serializers
from .models import EnglishAuctionItem, EnglishBid
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishAuctionItem
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishBid
        fields = '__all__'

