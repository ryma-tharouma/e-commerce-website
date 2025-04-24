import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Payment
from .forms import PaymentForm
from cart.models import CartItem,Order,OrderItem

def checkout(request):
    # session_id = request.session.session_key 
    # print(session_id)
    # cart_items = CartItem.objects.filter(session_id=session_id)
    # order = Order.objects.create(total_price=sum(item.quantity * item.product.price for item in cart_items))
    # for item in cart_items:
    #     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
    # print(order.total_price)
    # context = {
    #     'amount': order.total_price,
    #     'email': 'ferielakm@gmail.com',
    #     'payment_method': 'EDAHABIA'
    # }
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            session_id = request.session.session_key 
            print(session_id)
            cart_items = CartItem.objects.filter(session_id=session_id)
            order = Order.objects.create(total_price=sum(item.quantity * item.product.price for item in cart_items))
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            # Prepare data for Chargily API
            print(order.total_price)
            payload = {
                "client": payment.client,
                "client_email": payment.client_email,
                "invoice_number": payment.invoice_number,
                "amount": float(payment.amount),
                "discount": float(payment.discount),
                "back_url": settings.BACK_URL,
                "webhook_url": "https://webhook.site/2cc88d77-8137-43fd-95b1-9a095212fb23",
                "mode": payment.mode,
                "comment": payment.comment,
            }

            headers = {
                 "X-Authorization": settings.CHARGILY_API_KEY,  # Use X-Authorization instead of Authorization
                 "Content-Type": "application/json",
                 "Accept": "application/json"  # Add Accept header
            }


            response = requests.post(settings.CHARGILY_INVOICE_URL, json=payload, headers=headers)
            print(response.json())
            if response.status_code == 201:
                data = response.json()
                print(data)
                return redirect(data["checkout_url"])  # Redirect user to payment page
            else:
                return render(request, "payments/error.html", {"message": "Payment failed!"})

    else:
        form = PaymentForm()
    #cart_items.delete()
    #context['form'] = form
    return render(request, "payments/checkout.html", {"form": form})


def payment_success(request):
    return render(request, "payments/success.html")