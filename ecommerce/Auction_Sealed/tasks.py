from django_q.tasks import schedule
from django_q.models import Schedule
from django.utils import timezone
from .views import send_invoice_email, generate_invoice


def notify_winner(auction_id):
    from .models import SealedAuctionItem
    auction = SealedAuctionItem.objects.get(id=auction_id)

    if auction.winner==None:
        auction.determine_winner()
        
        print("sending an email Sealed auction")
        if auction.winner:
            print(auction.winner)

            # send_invoice_email(auction,auction.winner.email,generate_invoice(auction))
            send_invoice_email(auction,"nassabde227@gmail.com",generate_invoice(auction))
            
            print("sent ")
            auction.winner_notified = True
            auction.save()

        else :
                print("idk man ")
            

# Schedule this when creating/updating auctions
def schedule_auction_notification(auction):
    task_name = f"Sealed_auction_winner_notification_{auction.id}"

    # Check if a task already exists
    existing_task = Schedule.objects.filter(name=task_name).first()

    if not existing_task:
        
        schedule(
            'Sealed_Auction.tasks.notify_winner',
            auction.id,
            schedule_type='O',  # One-time
            name=f"Sealed_auction_winner_notification_{auction.id}",
            next_run=auction.end_time,
        )