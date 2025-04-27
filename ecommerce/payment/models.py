from django.db import models

class Payment(models.Model):
    # client = models.CharField(max_length=255,default='client')
    client = models.CharField(max_length=255, null=True, blank=True)

    client_email = models.EmailField()
    # client_email = models.EmailField(default="default@example.com")

    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mode = models.CharField(max_length=10, choices=[('EDAHABIA', 'EDAHABIA'), ('CIB', 'CIB')])
    comment = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client}"
