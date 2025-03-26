from django.urls import path
from django.urls import path
from .views import add_to_cart,remove_from_cart, get_cart, clear_cart, cart_page,create_checkout_session,get_products,success

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  
    path('view/', get_cart, name='get_cart'),
    path('clear/', clear_cart, name='clear_cart'),
    path('', cart_page, name='cart_page'),
    path("api/checkout-session/", create_checkout_session, name="checkout-session"),
    path('api/products/', get_products, name='get_products'),
    path('success/', success, name='success'),

]

