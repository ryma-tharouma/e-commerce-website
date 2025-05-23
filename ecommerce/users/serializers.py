from rest_framework import serializers
from django.contrib.auth import get_user_model
from Auction_English.models import EnglishBid

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'buyer')
        )
        return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'role']

class UserBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnglishBid
        fields = ['auction', 'amount', 'timestamp']

class UserProfileSerializer(serializers.ModelSerializer):
    bids = UserBidSerializer(many=True, read_only=True, source='english_auction_bidder')

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'bids']