from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import SealedAuctionItem, SealedBid
from .serializers import AuctionSerializer, BidSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User

import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework import status
from datetime import datetime
from Auction_English.views import get_fake_user
# from django.views.decorators.csrf import ensure_csrf_cookie
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import stripe
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags

# Create your views here.


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = SealedAuctionItem.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BidViewSet(viewsets.ModelViewSet):
    queryset = SealedBid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

class SealedAuctionDetailView(RetrieveAPIView):
    queryset = SealedAuctionItem.objects.all()
    serializer_class = AuctionSerializer

from decimal import Decimal
@api_view(["POST"])
def place_bid(request, id):
    try:
        auction = SealedAuctionItem.objects.get(id=id)
        bid_amount = Decimal(request.data.get("amount"))
        user_id = request.data.get("user")
        user= User.objects.get(id=user_id)
        print(f"the auction : {auction}\n the bid :{bid_amount}\n")

        if bid_amount is None or user is None:
            print("one of these is non ")
            return Response({"error": "Invalid data"}, status=400)


        
        bid = SealedBid(auction=auction, bidder=user, amount=bid_amount)
        bid.save()
        auction.save()
        print("placed sucesfuly")
        return Response({"message": "Bid placed successfully"})
    except SealedAuctionItem.DoesNotExist:
        return Response({"error": "Auction not found"}, status=404)
        

@api_view(['POST'])
@permission_classes([])  # Ajuste les permissions selon tes besoins
def create_auction(request):
    data = request.data
    images = request.FILES.getlist('images')  # Récupère toutes les images envoyées
    
    # Récupérer le vendeur (à ajuster selon l'authentification)
    # seller = User.objects.get(id=data.get('seller_id'))
    fake_user = get_fake_user()  
    
    # when i get user 
    # user_id = request.data.get("user")
    # user= User.objects.get(id=user_id) #user_id

    
    # Créer l'enchère sans images
    auction = SealedAuctionItem.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        seller=fake_user,
        starting_price=data.get('starting_price'),
        end_time=datetime.strptime(data.get('end_time'), "%Y-%m-%dT%H:%M") ,
        start_time=datetime.strptime(data.get('end_time'), "%Y-%m-%dT%H:%M")
    )
    
    # Créer un dossier pour stocker les images (ex: media/auctions/{auction.id}/)
    auction_folder = os.path.abspath(
        os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'imgs', 'Auction_Sealed', str(auction.id))
    )
    os.makedirs(auction_folder, exist_ok=True)
    
    for index, image in enumerate(images, start=1):  # Start index from 1
        fs = FileSystemStorage(location=auction_folder)
        filename = f"image{index}.jpg"  # Rename image (image1.jpg, image2.png, etc.)
        
        file_path = fs.save(filename, image)
        print(f"Saved: {file_path}")
        # Sauvegarde le chemin relatif dans la base de données si besoin (ex: Image model)
        
    return Response({"message": "Auction created successfully!", "auction_id": auction.id}, status=status.HTTP_201_CREATED)

# Génération de la facture PDF
def generate_invoice(Bid):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Bill_{Bid.id}.pdf")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "PAYEMNT BILL")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"ORDER ID: {Bid.id}")
    pdf.drawString(50, 750, f"Date: {Bid.auction.start_time.strftime('%Y-%m-%d %H:%M')}")

    pdf.line(50, 740, 550, 740)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 720, "Title")
    pdf.drawString(500, 720, "Total")

    y = 700
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, Bid.auction.title)
    pdf.drawString(400, y, f"{Bid.auction.Winning_price:.2f}€")
    y -= 20
    
    pdf.line(50, y - 10, 550, y - 10)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(400, y - 30, "Total:")
    pdf.drawString(500, y - 30, f"{Bid.auction.Winning_price:.2f}€")
    
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer



def send_invoice_email(auction,user_email , pdf_buffer):
    
    try:
        print(auction.id)
        subject = f"Your bill for the sealed auction N#{auction.id}"
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
from django.http import JsonResponse

@csrf_exempt
@api_view(['GET'])
def create_checkout_session(request,id ):
    
    try:
        # print(EnglishBid.objects.all().values('id', 'product', 'quantity', 'session_id'))
        print(f"payment function ")
        print(stripe.api_key    )

        session_id = request.session.session_key  # Récupérer l'ID de session
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            print(f"New session created: {session_id}")
        else:
            print(f"Existing session: {session_id}")

        # Filtrer les articles du panier avec session_id au lieu de user
        item = SealedBid.objects.get(id=id)
        print(f"Existing bid: {item}")

        if not item:
            return JsonResponse({'error': 'Votre panier est vide'}, status=400)

        
        # Génération du PDF après paiement
        invoice_pdf = generate_invoice(item)

        # Convertir les articles en format Stripe
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.auction.title,
                        'description': item.auction.description
                    },
                    'unit_amount': int(item.amount ),
                },
                'quantity': 1,
            }
        ]

        # Créer une session de paiement Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            # success_url=f'http://localhost:3000/Bids/',
            success_url=f'http://127.0.0.1:8000/Auction_Sealed/auctions/Bids/pay/success/{id}',
            cancel_url='http://127.0.0.1:8000/Auction_Sealed/auctions/Bids/pay/cancel/',

        )

  

        return JsonResponse({'id': checkout_session.id, 'url': checkout_session.url})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
def success(request,order_id):
    # order_id = request.GET.get('order_id')
    if not order_id:
        return HttpResponse("Order ID manquant", status=400)

    order = get_object_or_404(SealedBid, id=order_id)
    invoice_pdf = generate_invoice(order)
    send_invoice_email(order,"Nassabde227@gmail.com",  invoice_pdf)

    # response = HttpResponse(invoice_pdf.getvalue(), content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    # response['X-Redirect'] = 'http://localhost:3000/Bids'  # Header personnalisé
    # return response
    return redirect('http://localhost:3000/Bids')