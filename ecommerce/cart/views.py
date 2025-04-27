import json
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import CartItem, Product, Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .serializers import OrderSerializer, ProductSerializer,OrderItemSerializer
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Stripe Configuration
stripe.api_key = settings.STRIPE_SECRET_KEY
@api_view(['GET'])
def init_session(request):
    """
    Initialise une nouvelle session si elle n'existe pas
    """
    if not request.session.session_key:
        request.session.create()
        print(f"🆕 Session créée: {request.session.session_key}")
    return Response({
        'status': 'session initialized',
        'session_key': request.session.session_key
    })

def check_session(request):
    session_data = request.session.items()
    return JsonResponse({"session": dict(session_data)})

# def cart_page(request):
#     return render(request, 'cart/cart.html')

def list_cart(session_id):
    print("Session key après load dans list cart :", session_id)

    cart_items = CartItem.objects.filter(session_id=session_id)
    print(f"🛒 [DEBUG] Nombre d'items trouvés: {cart_items.count()}")
    for item in cart_items:
        print(f"Image du produit {item.product.name} : {item.product.image}")
    return [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image' : item.product.image,
            'subtotal': float(item.quantity * item.product.price)
        }
        for item in cart_items
    ]

# Génération de la facture PDF
def generate_invoice(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Facture_{order.id}.pdf")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "FACTURE D'ACHAT")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"Commande ID: {order.id}")
    pdf.drawString(50, 750, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")

    pdf.line(50, 740, 550, 740)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 720, "Produit")
    pdf.drawString(300, 720, "Quantité")
    pdf.drawString(400, 720, "Prix Unitaire")
    pdf.drawString(500, 720, "Total")

    y = 700
    pdf.setFont("Helvetica", 12)
    for item in order.items.all():
        pdf.drawString(50, y, item.product.name)
        pdf.drawString(300, y, str(item.quantity))
        pdf.drawString(400, y, f"{item.product.price:.2f}€")
        pdf.drawString(500, y, f"{item.subtotal():.2f}€")
        y -= 20
    
    pdf.line(50, y - 10, 550, y - 10)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(400, y - 30, "Total:")
    pdf.drawString(500, y - 30, f"{order.total_price:.2f}€")
    
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

# @api_view(['POST'])
# def add_to_cart(request, product_id):
#     #print("Cookies reçus :", request.COOKIES)  # 🔍 Vérifie si 'sessionid' est bien là
#     session_id = request.session.session_key
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.data.get('quantity', 1))
#     # print("🔑 Session actuelle dans add cart:", request.session.session_key)
#     # print("🔒 Cookies reçus dans add cart :", request.COOKIES)

#     print("Session key après load dans add to cart :", session_id)
#     if not session_id:
#         print("❌ Session introuvable, problème de cookie ?")
#         return Response({'error': 'Session non trouvée'}, status=400)

#     if product.stock < quantity:
#         return Response({'error': 'Stock insuffisant'}, status=400)

#     cart_item, created = CartItem.objects.get_or_create(
#             product=product,
#             session_id=session_id,
#             defaults={'quantity': 1}
#     )
#     if not created:
#         cart_item.quantity += quantity
#     cart_item.save()

#     product.stock -= quantity
#     product.save()

#     return Response({'message': 'Produit ajouté au panier', 'cart': list_cart(session_id)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    session_id = request.session.session_key
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.data.get('quantity', 1))

    print("Session key:", session_id)
    
    # Save CartItem with user if authenticated
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += quantity
    cart_item.save()

    product.stock -= quantity
    product.save()

    return Response({'message': 'Produit ajouté au panier','cart': list_cart(session_id)})



@api_view(['POST'])
def remove_from_cart(request, product_id):
    session_id = request.session.session_key
    if not session_id:
        return Response({'error': 'Session non trouvée'}, status=400)

    cart_item = CartItem.objects.filter(product_id=product_id, session_id=session_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        
        # Remettre le stock à jour
        cart_item.product.stock += 1
        cart_item.product.save()
        
        return Response({'message': 'Quantité réduite', 'cart': list_cart(session_id)})

    return Response({'error': 'Produit non trouvé'}, status=404)


@api_view(['POST'])
def clear_cart(request):
    session_id = request.session.session_key
    if not session_id:
        return Response({'error': 'Session non trouvée'}, status=400)
    cart_items = CartItem.objects.filter(session_id=session_id)
    for item in cart_items:
        item.product.stock += item.quantity
        item.product.save()
    cart_items.delete()
    return Response({'message': 'Panier vidé et stock restauré'})


@api_view(['GET'])
def get_cart(request):
    session_id = request.session.session_key
    print("session dans get cart : ",session_id)
    # print("🔑 Session actuelle dans get cart:", request.session.session_key)
    # print("🔒 Cookies reçus dans get cart :", request.COOKIES)

    if not session_id:
        return Response({'error': 'Session non trouvée'}, status=400)
    return Response(list_cart(session_id))

# views.py
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Product

@api_view(['POST'])
def create_product(request):
    if request.method == 'POST':
        # Initialize the serializer with the incoming data
        serializer = ProductSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the product if data is valid
            product = serializer.save()
            return Response({"message": "Product created successfully", "product_id": product.id}, status=201)
        else:
            # Return validation errors if data is invalid
            return Response({"error": serializer.errors}, status=400)
    return Response({"error": "Invalid request method"}, status=405)


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    data = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    return Response(data)

@csrf_exempt
@api_view(['GET'])
def create_checkout_session(request):
    try:
        print(CartItem.objects.all().values('id', 'product', 'quantity', 'session_id'))

        session_id = request.session.session_key  # Récupérer l'ID de session
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            print(f"New session created: {session_id}")
        else:
            print(f"Existing session: {session_id}")

        # Filtrer les articles du panier avec session_id au lieu de user
        cart_items = CartItem.objects.filter(session_id=session_id)
        print(f"Cart items for session {session_id}: {cart_items}")

        if not cart_items.exists():
            return JsonResponse({'error': 'Votre panier est vide'}, status=400)

        # Création de la commande
        order = Order.objects.create(total_price=sum(item.quantity * item.product.price for item in cart_items))

        # Ajouter les articles à la commande
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Génération du PDF après paiement
        invoice_pdf = generate_invoice(order)

        # Convertir les articles en format Stripe
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.product.name},
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in cart_items
        ]

        # Créer une session de paiement Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'http://127.0.0.1:8000/api/cart/success/?order_id={order.id}',
            cancel_url='http://127.0.0.1:8000//api/cart/cancel/',
        )

        # Supprimer le panier après paiement
        cart_items.delete()

        return JsonResponse({'id': checkout_session.id, 'url': checkout_session.url})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

def success(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return HttpResponse("Order ID manquant", status=400)

    order = get_object_or_404(Order, id=order_id)
    invoice_pdf = generate_invoice(order)
    send_invoice_email("ferielakm@gmail.com", order, invoice_pdf)

    response = HttpResponse(invoice_pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    response['X-Redirect'] = 'http://localhost:3000/cart'  # Header personnalisé
    return response


def send_invoice_email(user_email, order, pdf_buffer):
    try:
        print(order.id)
        subject = f"Votre facture pour la commande #{order.id}"
        html_message = render_to_string('cart/emails/invoice_email.html', {'order': order})
        plain_message = strip_tags(html_message)  # Version texte
        email = EmailMessage(subject, plain_message, settings.EMAIL_HOST_USER, [user_email])
        
        # Attacher le PDF
        email.attach(f"facture_{order.id}.pdf", pdf_buffer.getvalue(), "application/pdf")

        # Envoyer l'email
        email.send()
        print(f"✅ Facture envoyée à {user_email}")
    except Exception as e:
        print(f"❌ Erreur d'envoi d'email: {e}")



# @api_view(['POST'])
# def create_order(request):
#     # Assuming the user is authenticated
#     user = request.user  # Get the user from request
    
#     # 1. Get cart items for the user/session
#     cart_items = CartItem.objects.filter(session_id=request.session.session_key)
    
#     if not cart_items:
#         return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
    
#     # 2. Create an order
#     total_price = 0
#     order = Order.objects.create(total_price=total_price)
    
#     # 3. Add OrderItems for each cart item
#     for cart_item in cart_items:
#         product = cart_item.product
#         order_item = OrderItem.objects.create(
#             order=order,
#             product=product,
#             quantity=cart_item.quantity
#         )
#         total_price += order_item.subtotal()  # Update total price based on items
        
#     order.total_price = total_price  # Update order's total price
#     order.save()
    
#     # 4. Clear the cart
#     cart_items.delete()  # Clear cart after order is placed
    
#     # 5. Return the created order details
#     return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Important
def create_order(request):
    user = request.user  # Get the authenticated user from token

    # 1. Get cart items for the user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Create an order
    total_price = 0
    order = Order.objects.create(user=user, total_price=total_price)  # link order to user maybe?

    # 3. Add OrderItems for each cart item
    for cart_item in cart_items:
        product = cart_item.product
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart_item.quantity
        )
        total_price += order_item.subtotal()

    order.total_price = total_price
    order.save()

    # 4. Clear the cart
    cart_items.delete()

    # 5. Return the created order details
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
