from django.urls import path
from .views import checkout, payment_success

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("payment_success/", payment_success, name="payment_success"),
]
