from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import EnglishAuctionItem, EnglishBid
from .serializers import AuctionSerializer, BidSerializer
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework import status
from datetime import datetime
from decimal import Decimal

from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import stripe
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags


from Auction_Sealed.models import SealedBid
from Auction_Combinatoire.models import CombinatorialBid
# Stripe Configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = EnglishAuctionItem.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BidViewSet(viewsets.ModelViewSet):
    queryset = EnglishBid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnglishAuctionDetailView(RetrieveAPIView):
    queryset = EnglishAuctionItem.objects.all()
    serializer_class = AuctionSerializer

def get_fake_user():
    return User.objects.exclude(username="admin").first()


@api_view(["POST"])
def place_bid(request, id):
    try:
        auction = EnglishAuctionItem.objects.get(id=id)
        print(f"{request.data.get('amount')}")
        bid_amount = Decimal(request.data.get("amount"))
        user_id = request.data.get("user")
        user= User.objects.get(id=user_id)
        print(f"the auction : {auction}\n the bid :{bid_amount}\n")

        if bid_amount is None or user is None:
            print("one of these is non ")
            return Response({"error": "Invalid data"}, status=400)

        if float( bid_amount) <= float( auction.current_price):

            return Response({"error": "Your bid must be higher than the current price"}, status=400)
        
        bid = EnglishBid(auction=auction, bidder=user, amount=bid_amount)
        bid.save()
        auction.current_price = float(bid_amount)
        auction.save()
        print("placed sucesfuly")
        return Response({"message": "Bid placed successfully", "new_price": auction.current_price})
    except EnglishAuctionItem.DoesNotExist:
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
    auction = EnglishAuctionItem.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        seller=fake_user,
        starting_price=data.get('starting_price'),
        current_price=data.get('starting_price'),  # Initialise current_price
        end_time=datetime.strptime(data.get('end_time'), "%Y-%m-%dT%H:%M") ,
        start_time=datetime.strptime(data.get('end_time'), "%Y-%m-%dT%H:%M")
    )
    
    # Créer un dossier pour stocker les images (ex: media/auctions/{auction.id}/)
    auction_folder = os.path.abspath(
        os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'imgs', 'Auction_English', str(auction.id))
    )
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
def generate_invoice(Bid):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Bill_{Bid.auction.id}.pdf")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "PAYMENT BILL")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"Odre ID: {Bid.id}")
    pdf.drawString(50, 750, f"Date: {Bid.auction.start_time.strftime('%Y-%m-%d %H:%M')}")

    pdf.line(50, 740, 550, 740)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 720, "Title")
    pdf.drawString(500, 720, "Total")

    y = 700
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, Bid.auction.title)
    pdf.drawString(400, y, f"{Bid.auction.current_price:.2f}€")
    y -= 20
    
    pdf.line(50, y - 10, 550, y - 10)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(400, y - 30, "Total:")
    pdf.drawString(500, y - 30, f"{Bid.auction.current_price:.2f}€")
    
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer



def send_invoice_email(auction,user_email , pdf_buffer):
    
    try:
        print(auction.id)
        subject = f"Your bill for English auction N#{auction.id}"
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



def get_user_bids(request, user_id):
    try:
        # Fetch the user from the database
        user = User.objects.get(id=user_id)
        
        # Fetch bids for the user from all relevant models
        english_bids = EnglishBid.objects.filter(bidder=user)
        sealed_bids = SealedBid.objects.filter(bidder=user)
        combinatorial_bids = CombinatorialBid.objects.filter(user=user)
        
        english_bids_data = []
        if english_bids :
            for bid in english_bids:
                    english_bids_data.append({
                        'id': bid.id,
                        'auction_id': bid.auction.id,
                        'auction_title': bid.auction.title,
                        'amount': float(bid.amount),
                        
                    })
        

        sealed_bids_data = []
        if sealed_bids :
            for bid in sealed_bids:
                    sealed_bids_data.append({
                        'id': bid.id,
                        'auction_id': bid.auction.id,
                        'auction_title': bid.auction.title,
                        'amount': float(bid.amount),
                        
                    })
        

        Combinatorial_bids_data = []
        if combinatorial_bids:
            for bid in combinatorial_bids:
                product_list = []
                for product in bid.products.all():  # ✅ FIX ICI
                    product_list.append(product.name)
                Combinatorial_bids_data.append({
                    'id': bid.id,
                    'auction_id': bid.auction.id,
                    'auction_title': bid.auction.title,
                    'amount': float(bid.amount),
                    'products': product_list
                })
        

        # Return the data as a JSON response with separate sections

        return JsonResponse({

            'english_bids': english_bids_data,
            'sealed_bids': sealed_bids_data,
            'combinatorial_bids': Combinatorial_bids_data,
        }, status=200)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


from django.views.decorators.csrf import csrf_exempt
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
        item = EnglishBid.objects.get(id=id)
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
                    'unit_amount': int(item.auction.current_price ),
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
            success_url=f'http://127.0.0.1:8000/Auction_English/auctions/Bids/pay/success/{id}',
            cancel_url='http://127.0.0.1:8000/Auction_English/auctions/Bids/pay/cancel/',

        )

  

        return JsonResponse({'id': checkout_session.id, 'url': checkout_session.url})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

def success(request,order_id):
    # order_id = request.GET.get('order_id')
    
    if not order_id:
        return HttpResponse("Order ID manquant", status=400)

    order = get_object_or_404(EnglishBid, id=order_id)
    invoice_pdf = generate_invoice(order)
    send_invoice_email(order,"Nassabde227@gmail.com",  invoice_pdf)

    response = HttpResponse(invoice_pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{order.id}.pdf"'
    response['X-Redirect'] = 'http://localhost:3000/Bids'  # Header personnalisé
    return response
