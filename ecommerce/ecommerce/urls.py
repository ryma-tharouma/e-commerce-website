from django.contrib import admin
from django.urls import path,include
from Auction_English.views import get_user_bids,success

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/', include('cart.urls')), 
    path('Auction_English/', include('Auction_English.urls')),
    path('Auction_Sealed/', include('Auction_Sealed.urls')),
    path('Auction_Combinatoire/', include('Auction_Combinatoire.urls')),
    path('inventory/', include('inventory.urls')), 
    path('Bids/<int:user_id>', get_user_bids, name="get_user_bids"), 
    path('Bids/pay/success/<int:order_id>', success, name="success"),  
]
