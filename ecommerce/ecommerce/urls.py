"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Auction_English.views import get_user_bids,success
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cart/', include('cart.urls')),  # On inclut les URLs de l'application "cart"

    path('Auction_English/', include('Auction_English.urls')),
    path('Auction_Sealed/', include('Auction_Sealed.urls')),
    path('Auction_Combinatoire/', include('Auction_Combinatoire.urls')),
    path('Bids/<int:user_id>',get_user_bids, name="get_user_bids" ),
    path('Bids/pay/success/<int:order_id>',success, name="success" ),
    

]
