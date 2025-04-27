from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView 
from Auction_English.views import get_user_bids,success
from payment.views import checkout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/', include('cart.urls')),  # On inclut les URLs de l'application "cart"
    path('api/users/', include('users.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Auction_English/', include('Auction_English.urls')),
    path('Auction_Sealed/', include('Auction_Sealed.urls')),
    path('Auction_Combinatoire/', include('Auction_Combinatoire.urls')),
    path('Bids/<int:user_id>',get_user_bids, name="get_user_bids" ),
    path('Bids/pay/success/<int:order_id>',success, name="success" ),
    path('api/shipment/', include('shipment.urls')),
    path('payment/',include('payment.urls')),
    path('api/cart/', include('cart.urls')), 
    path('inventory/', include('inventory.urls')),  
    path('Bids/pay/success/<int:order_id>', success, name="success"),  

]
