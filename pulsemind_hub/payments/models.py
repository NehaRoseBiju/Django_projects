import uuid
from django.db import models
from django.conf import settings
from consultations.models import Appointment

class PaymentTransaction(models.Model):
    METHOD_CHOICES = (
        ('CARD', 'Credit / Debit Card'),
        ('UPI', 'UPI / QR Code'),
        ('NETBANKING', 'Net Banking'),
        ('WALLET', 'Digital Wallet'),
    )
    STATUS_CHOICES = (
        ('COMPLETED', 'Completed'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment_transaction')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments_made')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='CARD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.transaction_id[:8]} - ${self.amount} for Appt #{self.appointment.id}"
