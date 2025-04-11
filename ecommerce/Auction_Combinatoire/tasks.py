from django_q.tasks import schedule
from django_q.models import Schedule
from django.utils import timezone
from .views import send_invoice_email, generate_invoice


def notify_winner(auction_id):
    from .models import CombinatorialAuction
    auction = CombinatorialAuction.objects.get(id=auction_id)

    if auction.Winner_list==None:
        bids=auction.determine_winners()
        
        print("sending an email Combinatorial auction ")
        if auction.Winner_list:
            print(auction.Winner_list)
            for winner in auction.Winner_list :
                for bid in bids:
                    if bid.user == winner :
                        # send_invoice_email(auction,bid,auction.winner.email,generate_invoice(auction))
                        send_invoice_email(auction,bid,"nassabde227@gmail.com",generate_invoice(auction,bid))
            
            print("sent ")
            auction.winner_notified = True
            auction.save()

        else :
                print("idk man ")
            

# Schedule this when creating/updating auctions
def schedule_auction_notification(auction):
    task_name = f"Combinatorial_auction_winner_notification_{auction.id}"

    # Check if a task already exists
    existing_task = Schedule.objects.filter(name=task_name).first()

    if not existing_task:
        
        schedule(
            'Combinatorial_Auction.tasks.notify_winner',
            auction.id,
            schedule_type='O',  # One-time
            name=f"Combinatorial_auction_winner_notification_{auction.id}",
            next_run=auction.end_time,
        )