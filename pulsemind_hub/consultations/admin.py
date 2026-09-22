from django.contrib import admin
from consultations.models import DoctorSlot, Appointment

@admin.register(DoctorSlot)
class DoctorSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'is_booked']
    list_filter = ['date', 'is_booked']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment_date', 'fee', 'payment_status', 'status']
    list_filter = ['payment_status', 'status', 'appointment_date']
