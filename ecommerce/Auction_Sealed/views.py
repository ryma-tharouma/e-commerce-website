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
    auction_folder = os.path.join(settings.MEDIA_ROOT, f'./frontend/public/imgs/Sealed_Auction/{auction.id}')
    os.makedirs(auction_folder, exist_ok=True)
    
    for index, image in enumerate(images, start=1):  # Start index from 1
        fs = FileSystemStorage(location=auction_folder)
        extension = os.path.splitext(image.name)[1]  # Get file extension (e.g., .jpg, .png)
        filename = f"image{index}{extension}"  # Rename image (image1.jpg, image2.png, etc.)
        
        file_path = fs.save(filename, image)
        print(f"Saved: {file_path}")
        # Sauvegarde le chemin relatif dans la base de données si besoin (ex: Image model)
        
    return Response({"message": "Auction created successfully!", "auction_id": auction.id}, status=status.HTTP_201_CREATED)

# Génération de la facture PDF
def generate_invoice(auction):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Bill_{auction.id}.pdf")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "PAYEMNT BILL")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"ORDER ID: {auction.id}")
    pdf.drawString(50, 750, f"Date: {auction.start_time.strftime('%Y-%m-%d %H:%M')}")

    pdf.line(50, 740, 550, 740)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 720, "Title")
    pdf.drawString(500, 720, "Total")

    y = 700
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, auction.title)
    pdf.drawString(400, y, f"{auction.Winning_price:.2f}€")
    y -= 20
    
    pdf.line(50, y - 10, 550, y - 10)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(400, y - 30, "Total:")
    pdf.drawString(500, y - 30, f"{auction.Winning_price:.2f}€")
    
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
