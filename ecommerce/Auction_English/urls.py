from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet, BidViewSet,EnglishAuctionDetailView, place_bid,create_auction, create_checkout_session,success
router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)
router.register(r'bids', BidViewSet)

urlpatterns = [
    path('', include(router.urls)),

     path('auctions/<int:id>/', EnglishAuctionDetailView.as_view(), name='auction-detail'),
     path("auctions/<int:id>/bid/", place_bid, name="place_bid"),
     path("auctions/create_auction", create_auction, name="create_auction"),
     path("auctions/Bids/pay/<int:id>", create_checkout_session, name="eng_create_checkout_session"),
     path("auctions/Bids/pay/success/<int:order_id>", success, name="eng_success"),


]
