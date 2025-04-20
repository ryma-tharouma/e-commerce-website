from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuctionViewSet, BidViewSet, place_bid,SealedAuctionDetailView,create_auction,success,create_checkout_session


router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)
router.register(r'bids_sealed', BidViewSet)

urlpatterns = [
    path('', include(router.urls)),
 
    path('auctions/<int:pk>/', SealedAuctionDetailView.as_view(), name='auction-detail'),
     path("auctions/<int:id>/bid/", place_bid, name="place_bid"),
     path("auctions/create_auction", create_auction, name="create_auction"),
      path("auctions/Bids/pay/<int:id>", create_checkout_session, name="seal_create_checkout_session"),
     path("auctions/Bids/pay/success/<int:order_id>", success, name="seal_success"),




]
