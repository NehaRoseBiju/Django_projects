import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class DoctorSlot(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='available_slots',
        limit_choices_to={'role': 'DOCTOR'}
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"Dr. {self.doctor.username} | {self.date} @ {self.start_time.strftime('%H:%M')}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('PENDING', 'Payment Pending'),
        ('PAID', 'Paid & Confirmed'),
        ('REFUNDED', 'Refunded'),
    )
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='patient_appointments',
        limit_choices_to={'role': 'PATIENT'}
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='doctor_appointments',
        limit_choices_to={'role': 'DOCTOR'}
    )
    slot = models.OneToOneField(DoctorSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms_notes = models.TextField(blank=True, null=True, help_text="Brief notes on symptoms or health concern")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='PENDING')
    meeting_room_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"Appointment #{self.id}: {self.patient.username} with Dr. {self.doctor.username} on {self.appointment_date}"

    @property
    def is_joinable(self):
        # Allow joining room if appointment is paid and scheduled
        return self.payment_status == 'PAID' and self.status == 'SCHEDULED'
