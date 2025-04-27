from django.shortcuts import get_object_or_404
from .models import CombinatorialAuction, CombinatorialBid, Product,Combinatorial_Product
from rest_framework import viewsets, permissions
from rest_framework.generics import RetrieveAPIView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import AuctionSerializer
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework import status
from datetime import datetime
from Auction_English.views import get_fake_user
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from decimal import Decimal
import json

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = CombinatorialAuction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AuctionDetailView(RetrieveAPIView):
    queryset = CombinatorialAuction.objects.all()
    serializer_class = AuctionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def get_products_auction(request,id):
    # Get products that are NOT linked to any auction
    auction = get_object_or_404(CombinatorialAuction, id=id)
    products = auction.products.all()

    # Convert products to JSON format
    product_list = [{"id": p.id, "name": p.name, "description": p.description} for p in products]

    return JsonResponse({"products": product_list})   

    # products = auction.products.all().values("id", "name", "description")  # Adjust fields as needed
    
    # return JsonResponse({"products": list(products)}, status=200)


@api_view(['POST'])
@permission_classes([])  # Ajuste les permissions selon tes besoins
def create_Auction(request):
    data = request.data
    
    # Récupérer le vendeur (à ajuster selon l'authentification)
    # seller = User.objects.get(id=data.get('seller_id'))
    fake_user = get_fake_user()  
    
    # when i get user 
    # user_id = request.data.get("user")
    # user= User.objects.get(id=user_id) #user_id

    product_ids = request.data.get("products", "[]")  # Default to empty list as string
    print(product_ids)
        # Convert JSON string to a list if needed
    if isinstance(product_ids, str):
            product_ids = json.loads(product_ids)

        # Ensure it's a list
    if not isinstance(product_ids, list):
            return JsonResponse({"error": "Invalid products format"}, status=400)


    #  # Get available products (not already in an auction)
    products = Combinatorial_Product.objects.filter(id__in=product_ids, combinatorial_auctions__isnull=True)
    print(products)
            # Ensure all selected products are available
    if products.count() != len(product_ids):
                print("hey gurl error")
                return JsonResponse({"error": "One or more products are already in an auction"}, status=400)

    # Créer l'enchère sans images
    auction = CombinatorialAuction.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        seller=fake_user,
        end_time=datetime.strptime(data.get('end_time'), "%Y-%m-%dT%H:%M") ,
        start_time=datetime.strptime(data.get('end_time'), "%Y-%m-%dT%H:%M"),
    )
    # Assign products to the auction
    print("Products before setting:", products)  # Debugging
    auction.products.set(products)
    print("Products after setting:", list(auction.products.all()))  # Debugging

     
    return Response({"message": "Auction created successfully!", "auction_id": auction.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([])  # Ajuste les permissions selon tes besoins
def create_Product(request):
    data = request.data
    images = request.FILES.getlist('images')  # Récupère toutes les images envoyées
    
    # Récupérer le vendeur (à ajuster selon l'authentification)
    # seller = User.objects.get(id=data.get('seller_id'))
    fake_user = get_fake_user()  
    
    # when i get user 
    # user_id = request.data.get("user")
    # user= User.objects.get(id=user_id) #user_id

    
    # Créer l'enchère sans images
    product = Product.objects.create(
        name=data.get('title'),
        description=data.get('description'),
        seller=fake_user,
    )
    
    # Créer un dossier pour stocker les images 
    product_folder = os.path.abspath(
        os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'imgs', 'Auction_Combinatoire','Products', str(product.id))
    )
    os.makedirs(product_folder, exist_ok=True)
    
    for index, image in enumerate(images, start=1):  # Start index from 1
        fs = FileSystemStorage(location=product_folder)
        extension = os.path.splitext(image.name)[1]  # Get file extension (e.g., .jpg, .png)
        filename = f"image{index}.jpg"  # Rename image (image1.jpg, image2.png, etc.)
        
        file_path = fs.save(filename, image)
        print(f"Saved: {file_path}")
        # Sauvegarde le chemin relatif dans la base de données si besoin (ex: Image model)
        
    return Response({"message": "Product created successfully!", "product_id": product.id}, status=status.HTTP_201_CREATED)


def get_products(request):
    # Get products that are NOT linked to any auction
    assigned_products = CombinatorialAuction.objects.values_list("products", flat=True)
    unassigned_products = Product.objects.exclude(id__in=assigned_products)

    products = list(unassigned_products.values("id", "name", "description"))
    return JsonResponse(products, safe=False)

def get_combi_products(request):
    # Get products that are NOT linked to any auction
    assigned_products = CombinatorialAuction.objects.values_list("products", flat=True)
    unassigned_products = Combinatorial_Product.objects.exclude(id__in=assigned_products)

    products = list(unassigned_products.values("id", "name", "description"))
    return JsonResponse(products, safe=False)

@api_view(['POST'])
@permission_classes([])  # Ajuste les permissions selon tes besoins
def create_combi_Product(request):
    data = request.data
    images = request.FILES.getlist('images')  # Récupère toutes les images envoyées
    
    # Récupérer le vendeur (à ajuster selon l'authentification)
    # seller = User.objects.get(id=data.get('seller_id'))
    fake_user = get_fake_user()  
    
    # when i get user 
    # user_id = request.data.get("user")
    # user= User.objects.get(id=user_id) #user_id

    
    # Créer l'enchère sans images
    product = Combinatorial_Product.objects.create(
        name=data.get('title'),
        description=data.get('description'),
        seller=fake_user,
    )
    
    # Créer un dossier pour stocker les images 
    product_folder = os.path.abspath(
        os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'imgs', 'Auction_Combinatoire','Products', str(product.id))
    )
    os.makedirs(product_folder, exist_ok=True)
    
    for index, image in enumerate(images, start=1):  # Start index from 1
        fs = FileSystemStorage(location=product_folder)
        extension = os.path.splitext(image.name)[1]  # Get file extension (e.g., .jpg, .png)
        filename = f"image{index}.jpg"  # Rename image (image1.jpg, image2.png, etc.)
        
        file_path = fs.save(filename, image)
        print(f"Saved: {file_path}")
        # Sauvegarde le chemin relatif dans la base de données si besoin (ex: Image model)
        
    return Response({"message": "Product created successfully!", "product_id": product.id}, status=status.HTTP_201_CREATED)

from django.db import transaction
@csrf_exempt  
@api_view(['POST'])
def create_bid(request, auction_id):
        try:
            with transaction.atomic():
                data = request.data
                print("Data received:", data)
                user_id = data.get("user")
                user = get_fake_user()
                amount = Decimal(data.get("amount"))
                print("amount:",amount)
                product_ids = [product['id'] for product in data.get("products", [])]

                if not user_id or not amount or not product_ids:
                    return JsonResponse({"error": "Missing required fields"}, status=400)
                try:
                    auction = CombinatorialAuction.objects.get(id=auction_id)
                except CombinatorialAuction.DoesNotExist:
                    return JsonResponse({"error": "Auction not found"}, status=404)

            # Vérifier si l'utilisateur existe
            # try:
            #     user = User.objects.get(id=user_id)
            # except User.DoesNotExist:
            #     return JsonResponse({"error": "User not found"}, status=404)

            # Vérifier si les produits existent et appartiennent bien à cette enchère
                products = Combinatorial_Product.objects.filter(id__in=product_ids, combinatorial_auctions=auction)
                if products.count() != len(product_ids):
                    return JsonResponse({"error": "Invalid products for this auction"}, status=400)

                # Créer et enregistrer l'enchère
                bid = CombinatorialBid.objects.create(user=user, auction=auction, amount=amount)
                bid.products.set(products)
                print( "a save")
                bid.clean()
                bid.save()

                return JsonResponse({"message": "Bid placed successfully", "new_price": amount}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    


def generate_invoice(auction,bid):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Facture_{auction.id}.pdf")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "FACTURE D'ACHAT")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"Commande ID: {auction.id}")
    pdf.drawString(50, 750, f"Date: {auction.start_time.strftime('%Y-%m-%d %H:%M')}")

    pdf.line(50, 740, 550, 740)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 720, "Produit")

    y = 700
    pdf.setFont("Helvetica", 12)
    print("hi",bid.products)
    for item in bid.products.all():
        pdf.drawString(50, y, item.name)
        y -= 20
    
    pdf.line(50, y - 10, 550, y - 10)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(400, y - 30, "Total:")
    pdf.drawString(500, y - 30, f"{bid.amount:.2f}€")
    
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer

from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import stripe
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags


def send_invoice_email(auction,bid,user_email , pdf_buffer):
    
    try:
        print(auction.id)
        subject = f"Your bill for ordre N#{auction.id}"
        html_message = render_to_string('email/invoice_email.html', {'auction': auction})
        plain_message = strip_tags(html_message)  # Version texte
        email = EmailMessage(subject, plain_message, settings.EMAIL_HOST_USER, [user_email])
        
        # Attacher le PDF
        email.attach(f"Bill_{auction.id}.pdf", pdf_buffer.getvalue(), "application/pdf")

        # Envoyer l'email
        email.send()
        print(f"✅ Facture envoyée à {user_email}")
    except Exception as e:
        print(f"❌ Erreur d'envoi d'email: {e}")



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404


@csrf_exempt
@api_view(['GET'])
def create_checkout_session(request, id):
    try:
        print("✅ Starting payment session creation")
        bid = CombinatorialBid.objects.get(id=id)
        print(bid.products)

        auction = bid.auction
        products = bid.products.all()

        if not products.exists():
            return JsonResponse({'error': 'Aucun produit dans cette enchère.'}, status=400)

        # Prix réparti également entre les produits
        price_per_product = float(bid.amount) / products.count()
        price_cents = int(price_per_product * 100)

        line_items = []
        for product in products:
            print("hi",bid.amount)
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                        'description': product.description ,
                    },
                    'unit_amount':int(bid.amount)*100 ,
                },
                'quantity': 1,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'http://127.0.0.1:8000/Auction_Combinatoire/auctions/Bids/pay/success/{bid.id}',
            cancel_url='http://127.0.0.1:8000/Auction_Combinatoire/auctions/Bids/pay/cancel/',
        )

        return JsonResponse({'id': checkout_session.id, 'url': checkout_session.url})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



from django.http import HttpResponse
from django.shortcuts import get_object_or_404
def success(request, order_id):
    if not order_id:
        return HttpResponse("Order ID manquant", status=400)

    bid = get_object_or_404(CombinatorialBid, id=order_id)
    invoice_pdf = generate_invoice(bid.auction,bid)
    send_invoice_email(bid.auction,bid, "Nassabde227@gmail.com", invoice_pdf)

    response = HttpResponse(invoice_pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_combinatoire_{bid.id}.pdf"'
    response['X-Redirect'] = 'http://localhost:3000/Bids'
    return response