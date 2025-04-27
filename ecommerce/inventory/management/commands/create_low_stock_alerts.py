from django.core.management.base import BaseCommand
from cart.models import Product
from inventory.models import LowStockAlert


class Command(BaseCommand):
    help = 'Creates low stock alerts for all products that don\'t have one'

    def handle(self, *args, **options):
        # Get all products that don't have a low stock alert
        products_without_alerts = Product.objects.filter(low_stock_alert__isnull=True)
        
        # Create alerts for these products
        for product in products_without_alerts:
            LowStockAlert.objects.create(product=product)
            self.stdout.write(self.style.SUCCESS(f'Created low stock alert for {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {products_without_alerts.count()} low stock alerts')) 