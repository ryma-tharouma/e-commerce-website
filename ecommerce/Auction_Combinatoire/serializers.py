from rest_framework import serializers
from .models import CombinatorialAuction,CombinatorialBid, Combinatorial_Product

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombinatorialAuction
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombinatorialBid
        fields = '__all__'

