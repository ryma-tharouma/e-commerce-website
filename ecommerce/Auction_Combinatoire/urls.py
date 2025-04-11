from django.urls import path
from .views import create_Product, get_products,create_Auction,AuctionDetailView,AuctionViewSet,get_products_auction,create_bid

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)
# router.register(r'bids', BidViewSet)

urlpatterns = [
    path('', include(router.urls)),


     path('auctions/<int:id>/', AuctionDetailView.as_view(), name='auction-detail'), 
     path('auctions/<int:id>/products', get_products_auction, name='auction-products'), 
     path("auctions/create_product", create_Product, name="create_product"),
     path("auctions/create_auction", create_Auction, name="create_auction"),
     path("auctions/<int:auction_id>/bid/", create_bid, name="create_bid"),
     path("get_products", get_products, name="get_products"),


]
