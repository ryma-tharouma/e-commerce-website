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


# Stripe Configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

def cart_page(request):
    return render(request, 'cart/cart.html')

def list_cart(session_id):
    cart_items = CartItem.objects.filter(session_id=session_id)
    return [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
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

@api_view(['POST'])
def add_to_cart(request, product_id):
    print("hereA")
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.data.get('quantity', 1))
    print("hereB")
    session_id = request.session.session_key
    print("hereC")
    if not session_id:
        print("here")
        request.session.create()
        session_id = request.session.session_key
    # if not session_id:
    #     print("here")
    #     request.session.save()

    if product.stock < quantity:
        return Response({'error': 'Stock insuffisant'}, status=400)

    cart_item, created = CartItem.objects.get_or_create(
            product=product,
            session_id=session_id,
            defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += quantity
    cart_item.save()

    product.stock -= quantity
    product.save()

    return Response({'message': 'Produit ajouté au panier', 'cart': list_cart(session_id)})

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

# @api_view(['GET'])
# @csrf_exempt
# def get_cart(request):
#     if not request.session.session_key:
#         request.session.save()  # Changez create() par save()
#         print(f"🔄 Session initialisée: {request.session.session_key}")
#     else:
#         print(f"🔁 Session existante: {request.session.session_key}")
    
#     cart_data = list_cart(request.session.session_key)
#     response = Response(cart_data)
    
#     if not request.COOKIES.get('sessionid'):
#         response.set_cookie(
#             key='sessionid',
#             value=request.session.session_key,
#             max_age=60*60*24*14,  # 2 semaines
#             httponly=True,
#             samesite='Lax',
#             secure=False,
#             path='/'
#         )
#     return response 

@api_view(['GET'])
def get_cart(request):
    session_id = request.session.session_key
    if not session_id:
        return Response({'error': 'Session non trouvée'}, status=400)
    return Response(list_cart(session_id))

# @api_view(['GET'])
# def get_cart(request):
#     if not request.session.session_key:
#         request.session.create()  # Force la création d'une session
#         print("💡 Nouvelle session créée:", request.session.session_key)

#     print(f"📌 Session ID: {request.session.session_key}")  # Debug

#     if not request.session.session_key:
#         return Response({'error': 'Session non trouvée'}, status=400)

#     return Response(list_cart(request.session.session_key))


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    data = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    return Response(data)

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



def success(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return HttpResponse("Order ID manquant", status=400)

    order = get_object_or_404(Order, id=order_id)
    
    # Générer la facture PDF
    invoice_pdf = generate_invoice(order)

    # Envoyer l'email avec la facture
    send_invoice_email("ferielakm@gmail.com", order, invoice_pdf)

    # Retourner le PDF en téléchargement
    response = HttpResponse(invoice_pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    return response


def send_invoice_email(user_email, order, pdf_buffer):
    try:
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











# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django.shortcuts import get_object_or_404
# from .models import Product
# from django.http import JsonResponse
# from django.conf import settings
# from django.http import JsonResponse
# import stripe
# from django.http import JsonResponse, FileResponse
# from .models import CartItem, Product, Order, OrderItem
# from io import BytesIO
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import simpleSplit
# import datetime
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAdminUser




# # Create your views here.


# # @api_view(['POST'])
# # @authentication_classes([SessionAuthentication, BasicAuthentication])
# # @permission_classes([IsAuthenticated])
# # def add_to_cart(request, product_id):
# #     product = get_object_or_404(Product, id=product_id)
# #     quantity = int(request.data.get('quantity', 1))
# #     user = request.user  

# #     # Vérifier si le stock est suffisant
# #     if product.stock < quantity:
# #         return Response({'error': 'Stock insuffisant'}, status=400)

# #     # Ajouter au panier ou mettre à jour la quantité
# #     cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

# #     if not created:
# #         if product.stock < (cart_item.quantity + quantity):
# #             return Response({'error': 'Stock insuffisant'}, status=400)
# #         cart_item.quantity += quantity  # Augmenter la quantité
# #     else:
# #         cart_item.quantity = quantity  # Définir la quantité
    
# #     cart_item.save()

# #     # Mettre à jour le stock du produit
# #     product.stock -= quantity
# #     product.save()

# #     return Response({'message': 'Produit ajouté au panier', 'cart': list_cart(user)})

# # @api_view(['GET'])
# # @authentication_classes([SessionAuthentication, BasicAuthentication])
# # @permission_classes([IsAuthenticated])
# # def get_cart(request):
# #     user = request.user
# #     cart = list_cart(user)
    
# #     return Response({
# #         'cart': cart,
# #         'total_items': sum(item['quantity'] for item in cart),
# #         'total_price': sum(item['subtotal'] for item in cart)
# #     })


# # @api_view(['POST'])
# # @authentication_classes([SessionAuthentication, BasicAuthentication])
# # @permission_classes([IsAuthenticated])
# # def clear_cart(request):
# #     user = request.user
# #     cart_items = CartItem.objects.filter(user=user)

# #     # Remettre les quantités en stock
# #     for item in cart_items:
# #         item.product.stock += item.quantity
# #         item.product.save()
    
# #     cart_items.delete()
# #     return Response({'message': 'Panier vidé et stock mis à jour'})


# # @api_view(['POST'])
# # @authentication_classes([SessionAuthentication, BasicAuthentication])
# # @permission_classes([IsAuthenticated])
# # def remove_from_cart(request, product_id):
# #     user = request.user
# #     cart_item = CartItem.objects.filter(user=user, product_id=product_id).first()

# #     if cart_item:
# #         product = cart_item.product
# #         product.stock += cart_item.quantity  # Restaurer le stock
# #         product.save()

# #         cart_item.delete()
# #         return Response({'message': 'Produit supprimé du panier', 'cart': list_cart(user)})
    
# #     return Response({'error': 'Produit non trouvé dans le panier'}, status=404)


# def cart_page(request):
#     return render(request, 'cart/cart.html')


# def list_cart():
#     cart_items = CartItem.objects.filter()
#     return [
#         {
#             'product_id': item.product.id,
#             'name': item.product.name,
#             'price': float(item.product.price),
#             'quantity': item.quantity,
#             'subtotal': float(item.quantity * item.product.price)
#         }
#         for item in cart_items
#     ]

# stripe.api_key = settings.STRIPE_SECRET_KEY  

# #avant pdf
# # def create_checkout_session(request):
# #     try:
# #         user = request.user
# #         cart_items = CartItem.objects.filter(user=user)

# #         if not cart_items.exists():
# #             return JsonResponse({'error': 'Votre panier est vide'}, status=400)

# #         # Convertir les articles en format Stripe
# #         line_items = [
# #             {
# #                 'price_data': {
# #                     'currency': 'usd',
# #                     'product_data': {'name': item.product.name},
# #                     'unit_amount': int(item.product.price * 100),
# #                 },
# #                 'quantity': item.quantity,
# #             }
# #             for item in cart_items
# #         ]

# #         # Créer une session de paiement Stripe
# #         checkout_session = stripe.checkout.Session.create(
# #             payment_method_types=['card'],
# #             line_items=line_items,
# #             mode='payment',
# #             success_url='http://127.0.0.1:8000/success/',
# #             cancel_url='http://127.0.0.1:8000/cancel/',
# #         )

# #         # Optionnel : Vider le panier après paiement
# #         cart_items.delete()

# #         return JsonResponse({'id': checkout_session.id})
# #     except Exception as e:
# #         return JsonResponse({'error': str(e)}, status=500)
    



# stripe.api_key = settings.STRIPE_SECRET_KEY  

# # Fonction pour générer une facture PDF
# def generate_invoice(order):
#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer, pagesize=A4)
#     pdf.setTitle(f"Facture_{order.id}.pdf")

#     # En-tête
#     pdf.setFont("Helvetica-Bold", 16)
#     pdf.drawString(200, 800, "FACTURE D'ACHAT")

#     pdf.setFont("Helvetica", 12)
#     pdf.drawString(50, 770, f"Commande ID: {order.id}")
#     pdf.drawString(50, 750, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")

#     # Ligne de séparation
#     pdf.line(50, 740, 550, 740)

#     # Colonnes
#     pdf.setFont("Helvetica-Bold", 12)
#     pdf.drawString(50, 720, "Produit")
#     pdf.drawString(300, 720, "Quantité")
#     pdf.drawString(400, 720, "Prix Unitaire")
#     pdf.drawString(500, 720, "Total")

#     y = 700
#     pdf.setFont("Helvetica", 12)

#     # Contenu
#     for item in order.items.all():
#         pdf.drawString(50, y, item.product.name)
#         pdf.drawString(300, y, str(item.quantity))
#         pdf.drawString(400, y, f"{item.product.price:.2f}€")
#         pdf.drawString(500, y, f"{item.subtotal():.2f}€")
#         y -= 20

#     # Ligne de séparation
#     pdf.line(50, y - 10, 550, y - 10)

#     # Total
#     pdf.setFont("Helvetica-Bold", 14)
#     pdf.drawString(400, y - 30, "Total:")
#     pdf.drawString(500, y - 30, f"{order.total_price:.2f}€")

#     pdf.showPage()
#     pdf.save()

#     buffer.seek(0)
#     return buffer

# # Vue pour télécharger la facture
# @api_view(['GET'])
# def download_invoice(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     pdf_buffer = generate_invoice(order)
#     return FileResponse(pdf_buffer, as_attachment=True, filename=f"facture_{order.id}.pdf")

# # Paiement Stripe + Création de la commande + Facture
# # def create_checkout_session(request):
# #     try:
# #         user = request.user
# #         cart_items = CartItem.objects.filter(user=user)

# #         if not cart_items.exists():
# #             return JsonResponse({'error': 'Votre panier est vide'}, status=400)

# #         # Création de la commande
# #         order = Order.objects.create(total_price=sum(item.quantity * item.product.price for item in cart_items))

# #         # Ajouter les articles à la commande
# #         for item in cart_items:
# #             OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

# #         # Génération du PDF après paiement
# #         invoice_pdf = generate_invoice(order)

# #         # Convertir les articles en format Stripe
# #         line_items = [
# #             {
# #                 'price_data': {
# #                     'currency': 'usd',
# #                     'product_data': {'name': item.product.name},
# #                     'unit_amount': int(item.product.price * 100),
# #                 },
# #                 'quantity': item.quantity,
# #             }
# #             for item in cart_items
# #         ]

# #         # Créer une session de paiement Stripe
# #         checkout_session = stripe.checkout.Session.create(
# #             payment_method_types=['card'],
# #             line_items=line_items,
# #             mode='payment',
# #             success_url=f'http://127.0.0.1:8000/success/?order_id={order.id}',
# #             cancel_url='http://127.0.0.1:8000/cancel/',
# #         )

# #         # Supprimer le panier après paiement
# #         cart_items.delete()

# #         return JsonResponse({'id': checkout_session.id})
# #     except Exception as e:
# #         return JsonResponse({'error': str(e)}, status=500)

# def send_invoice_email(user_email, order, pdf_buffer):
#     try:
#         subject = f"Votre facture pour la commande #{order.id}"
#         html_message = render_to_string('emails/invoice_email.html', {'order': order})
#         plain_message = strip_tags(html_message)  # Version texte
#         email = EmailMessage(subject, plain_message, settings.EMAIL_HOST_USER, [user_email])
        
#         # Attacher le PDF
#         email.attach(f"facture_{order.id}.pdf", pdf_buffer.getvalue(), "application/pdf")

#         # Envoyer l'email
#         email.send()
#         print(f"✅ Facture envoyée à {user_email}")
#     except Exception as e:
#         print(f"❌ Erreur d'envoi d'email: {e}")


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  # Nécessite une connexion utilisateur
# def create_checkout_session(request):
#     try:
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)

#         if not cart_items.exists():
#             return JsonResponse({'error': 'Votre panier est vide'}, status=400)

#         # Création de la commande
#         order = Order.objects.create(total_price=sum(item.quantity * item.product.price for item in cart_items))

#         # Ajouter les articles à la commande
#         for item in cart_items:
#             OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

#         # Générer la facture PDF
#         invoice_pdf = generate_invoice(order)

#         # Envoyer la facture par email
#         send_invoice_email(user.email, order, invoice_pdf)

#         # Convertir les articles en format Stripe
#         line_items = [
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {'name': item.product.name},
#                     'unit_amount': int(item.product.price * 100),
#                 },
#                 'quantity': item.quantity,
#             }
#             for item in cart_items
#         ]

#         # Créer une session de paiement Stripe
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=f'http://127.0.0.1:8000/success/?order_id={order.id}',
#             cancel_url='http://127.0.0.1:8000/cancel/',
#         )

#         # Supprimer le panier après paiement
#         cart_items.delete()

#         return JsonResponse({'id': checkout_session.id})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# @api_view(['POST'])
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.data.get('quantity', 1))

#     if product.stock < quantity:
#         return Response({'error': 'Stock insuffisant'}, status=400)

#     cart_item, created = CartItem.objects.get_or_create(product=product)
    
#     if not created:
#         if product.stock < cart_item.quantity + quantity:
#             return Response({'error': 'Stock insuffisant'}, status=400)
#         cart_item.quantity += quantity
#     else:
#         cart_item.quantity = quantity

#     cart_item.save()

#     # ✅ Met à jour le stock
#     product.stock -= quantity
#     product.save()

#     return Response({'message': 'Produit ajouté au panier', 'cart': list_cart()})


# @api_view(['POST'])
# def clear_cart(request):
#     cart_items = CartItem.objects.all()

#     for item in cart_items:
#         item.product.stock += item.quantity  # 🔄 Restaurer le stock
#         item.product.save()

#     cart_items.delete()  # 🚮 Supprimer tous les articles du panier

#     return Response({'message': 'Panier vidé et stock restauré'})

# @api_view(['GET'])
# def get_cart(request):
#     return Response(list_cart())  # Pas de filtre utilisateur

# @api_view(['POST'])
# def remove_from_cart(request, product_id):
#     cart_item = CartItem.objects.filter(product_id=product_id).first()

#     if cart_item:
#         cart_item.product.stock += cart_item.quantity  # 🔄 Restaurer le stock
#         cart_item.product.save()
#         cart_item.delete()  # 🚮 Supprimer du panier

#         return Response({'message': 'Produit supprimé du panier et stock restauré', 'cart': list_cart()})
    
#     return Response({'error': 'Produit non trouvé dans le panier'}, status=404)

# @api_view(['GET'])
# def get_products(request):
#     products = Product.objects.all()
#     data = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
#     return Response(data)

