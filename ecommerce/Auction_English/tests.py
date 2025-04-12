from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import EnglishAuctionItem, EnglishBid
from django.contrib.auth.models import User

# Create your tests here.
class AuctionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.auction = EnglishAuctionItem.objects.create(
            title='Test Auction',
            description='A test auction.',
            starting_price=10.00,
            current_price=10.00,
            end_time='2025-12-31T23:59:59Z',
            seller=self.user
        )

    def test_create_auction(self):
        data = {
            'title': 'New Auction',
            'description': 'Another auction.',
            'starting_price': 20.00,
            'current_price': 20.00,
            'end_time': '2025-12-31T23:59:59Z',
            'seller': self.user.id
        }
        response = self.client.post(reverse('auction-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_place_bid(self):
        bid_data = {
            'auction': self.auction.id,
            'bidder': self.user.id,
            'amount': 15.00
        }
        response = self.client.post(reverse('bid-list'), bid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
