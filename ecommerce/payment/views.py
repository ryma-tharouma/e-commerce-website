import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Payment
from .forms import PaymentForm
from cart.models import CartItem,Order,OrderItem
from datetime import datetime
from random import randint


def checkout(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    cart_items = CartItem.objects.filter(session_id=session_id)

    total_price = sum(item.quantity * item.product.price for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    now = datetime.now()
    invoice_number = f"INV-{now.strftime('%Y%m%d')}-{randint(1000, 9999)}"

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()

            order = Order.objects.create(total_price=total_price)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            payload = {
                "client": payment.client,
                "client_email": payment.client_email,
                "invoice_number": payment.invoice_number,
                "amount": float(payment.amount),
                "discount": float(payment.discount),
                "back_url": settings.BACK_URL,
                "webhook_url": "https://webhook.site/117d748e-79ab-4625-a7b0-845db6641bf4",
                "mode": payment.mode,
                "comment": payment.comment,
            }

            headers = {
                "X-Authorization": settings.CHARGILY_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            response = requests.post(settings.CHARGILY_INVOICE_URL, json=payload, headers=headers)
            print(response.json())
            if response.status_code == 201:
                data = response.json()
                return redirect(data["checkout_url"])
            else:
                return render(request, "payments/error.html", {"message": "Payment failed!"})
    else:
        form = PaymentForm(initial={"amount": total_price,"discount":quantity,"client_email":'ferielakm@gmail.com',"invoice_number":invoice_number})
    cart_items.delete()
    return render(request, "payments/checkout.html", {"form": form})


def payment_success(request):
    return render(request, "payments/success.html")