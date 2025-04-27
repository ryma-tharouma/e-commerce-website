from django.urls import path
from django.urls import path
from .views import check_session, create_order, create_product,init_session,add_to_cart,remove_from_cart, get_cart, clear_cart,create_checkout_session,get_products,success

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),  
    path('view/', get_cart, name='get_cart'),
    path('clear/', clear_cart, name='clear_cart'),
    path('init/', init_session, name='init-session'),
    path('checksessions/', check_session, name='init-session'),
    #path('', cart_page, name='cart_page'),
    path("api/checkout-session/", create_checkout_session, name="checkout-session"),
    path('api/products/', get_products, name='get_products'),
    path('success/', success, name='success'),
    # path('create-product/', create_product, name='create_product'),
    path('api/create_product/', create_product, name='create_product'),
    # path('order/create/', create_order, name='create_order'),
    path('order/create/', create_order, name='create_order')
]

