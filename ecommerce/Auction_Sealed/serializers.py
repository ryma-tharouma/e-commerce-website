from rest_framework import serializers
from .models import SealedAuctionItem, SealedBid
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SealedAuctionItem
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = SealedBid
        fields = '__all__'