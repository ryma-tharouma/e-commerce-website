from django.urls import path
from .views import create_product_view,product_delivery_api, create_shipment

urlpatterns = [
    path('product-delivery/', product_delivery_api, name='product_delivery_api'),
    path('product-delivery/<int:product_id>/', create_product_view, name='create_product_view'),
    path('create/<int:order_id>/', create_shipment, name='create-shipment'),
]
