from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PATIENT')
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True, help_text="For Doctors: e.g., Cardiologist, Psychiatrist, General Physician")
    qualification = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. MBBS, MD, PhD")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00, help_text="Fee charged per consultation (₹)")
    experience_years = models.PositiveIntegerField(default=5, help_text="Years of medical practice")
    wellness_goal = models.CharField(max_length=255, blank=True, null=True, default="Improve daily sleep and stay hydrated")
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        if self.is_admin or self.is_superuser:
            return f"Admin ({self.username})"
        role_prefix = f"Dr. {self.get_full_name() or self.username}" if self.role == 'DOCTOR' else (self.get_full_name() or self.username)
        return f"{role_prefix} ({self.get_role_display()})"
    
    @property
    def is_doctor(self):
        return self.role == 'DOCTOR'

    @property
    def is_patient(self):
        return self.role == 'PATIENT'

    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser or self.is_staff
