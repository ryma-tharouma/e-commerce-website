from django.urls import path
from .views import create_combi_Product, get_combi_products,create_Auction,AuctionDetailView,AuctionViewSet,get_products_auction,create_bid, create_checkout_session, success

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet)
# router.register(r'bids', BidViewSet)

urlpatterns = [
    path('', include(router.urls)),


     path('auctions/<int:id>/', AuctionDetailView.as_view(), name='auction-detail'), 
     path('auctions/<int:id>/products', get_products_auction, name='auction-products'), 
     path("auctions/create_product", create_combi_Product, name="create_product"),
     path("auctions/create_auction", create_Auction, name="create_auction"),
     path("auctions/<int:auction_id>/bid/", create_bid, name="create_bid"),
     path("get_products", get_combi_products, name="get_products"),
    path("auctions/Bids/pay/<int:id>", create_checkout_session, name="comb_create_checkout_session"),
     path("auctions/Bids/pay/success/<int:order_id>", success, name="comb_success"),


]
