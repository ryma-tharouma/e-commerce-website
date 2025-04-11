from django_q.tasks import schedule, Task
from django_q.models import Schedule
from django.core.mail import send_mail
from django.utils import timezone
from .views import send_invoice_email, generate_invoice


def notify_winner(auction_id):
    from .models import EnglishAuctionItem
    auction = EnglishAuctionItem.objects.get(id=auction_id)
    if auction.winner==None:
        auction.determine_winner()
        
        print("sending an email English auction ")
        if auction.winner:
            print(auction.winner)

            # send_invoice_email(auction,auction.winner.email,generate_invoice(auction))
            send_invoice_email(auction,"nassabde227@gmail.com",generate_invoice(auction))
            
            print("sent ")
            auction.winner_notified = True
            auction.save()

      
# Schedule this when creating/updating auctions
def schedule_auction_notification(auction):
    print('scheduled this')
    task_name = f"English_auction_winner_notification_{auction.id}"

    # Check if a task already exists
    existing_task = Schedule.objects.filter(name=task_name).first()

    if not existing_task:
        
        schedule(
            'English_Auction.tasks.notify_winner',
            auction.id,
            schedule_type='O',  # One-time
            name=f"English_auction_winner_notification_{auction.id}",
            next_run=auction.end_time,
        )