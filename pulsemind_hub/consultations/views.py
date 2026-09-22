import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import CustomUser
from .models import DoctorSlot, Appointment
from payments.models import PaymentTransaction

@login_required
def doctor_directory(request):
    specialty_query = request.GET.get('specialty', '').strip()
    search_query = request.GET.get('search', '').strip()

    doctors = CustomUser.objects.filter(role='DOCTOR', is_superuser=False).exclude(username='admin')
    if specialty_query:
        doctors = doctors.filter(specialization__icontains=specialty_query)
    if search_query:
        doctors = doctors.filter(username__icontains=search_query) | doctors.filter(first_name__icontains=search_query) | doctors.filter(last_name__icontains=search_query)

    context = {
        'doctors': doctors,
        'specialty_query': specialty_query,
        'search_query': search_query,
    }
    return render(request, 'consultations/doctor_directory.html', context)


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='DOCTOR')

    all_slots = DoctorSlot.objects.filter(doctor=doctor, date__gte=timezone.now().date()).order_by('date', 'start_time')
    available_slots_count = all_slots.filter(is_booked=False).count()

    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        symptoms = request.POST.get('symptoms_notes', '')

        if not slot_id:
            messages.error(request, "Please select an available consultation time slot.")
            return redirect('consultations:book', doctor_id=doctor.id)

        slot = get_object_or_404(DoctorSlot, id=slot_id, doctor=doctor)
        if slot.is_booked:
            messages.error(request, "Sorry, this time slot has already been booked. Please select an available slot.")
            return redirect('consultations:book', doctor_id=doctor.id)

        slot.is_booked = True
        slot.save()
        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            slot=slot,
            appointment_date=slot.date,
            appointment_time=slot.start_time,
            symptoms_notes=symptoms,
            fee=doctor.consultation_fee,
            status='SCHEDULED',
            payment_status='PENDING',
            meeting_room_id=str(uuid.uuid4())
        )

        messages.info(request, f"Appointment initialized! Please complete payment of ₹{doctor.consultation_fee} to confirm your booking.")
        return redirect('payments:checkout', appointment_id=appointment.id)

    context = {
        'doctor': doctor,
        'slots': all_slots,
        'available_slots_count': available_slots_count,
    }
    return render(request, 'consultations/book_appointment.html', context)


@login_required
def video_room(request, room_id):
    appointment = get_object_or_404(Appointment, meeting_room_id=room_id)

    if request.user != appointment.patient and request.user != appointment.doctor:
        messages.error(request, "Unauthorized access to video consultation room.")
        return redirect('dashboard:index')

    if appointment.payment_status != 'PAID':
        messages.error(request, "Payment is pending for this appointment. Please complete payment first.")
        return redirect('payments:checkout', appointment_id=appointment.id)

    context = {
        'appointment': appointment,
        'room_id': room_id,
        'is_doctor': request.user == appointment.doctor,
    }
    return render(request, 'consultations/video_room.html', context)


@login_required
def my_consultations(request):
    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.filter(patient=request.user)

    return render(request, 'consultations/my_consultations.html', {'appointments': appointments})


@login_required
def manage_slots(request):
    """Allows doctors and admins to view, create, and manage consultation time slots."""
    if not request.user.is_doctor and not request.user.is_admin:
        messages.error(request, "Only Doctors and Administrators can manage consultation slots.")
        return redirect('dashboard:index')

    doctor = request.user
    if request.user.is_admin and request.GET.get('doctor_id'):
        doctor = get_object_or_404(CustomUser, id=request.GET.get('doctor_id'), role='DOCTOR')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')

            if date_str and start_time_str and end_time_str:
                DoctorSlot.objects.create(
                    doctor=doctor,
                    date=date_str,
                    start_time=start_time_str,
                    end_time=end_time_str
                )
                messages.success(request, f"New consultation time slot added for {date_str} ({start_time_str} - {end_time_str})!")
            else:
                messages.error(request, "Please fill in all required slot fields.")

        elif action == 'block_leave':
            leave_date_str = request.POST.get('leave_date')
            if leave_date_str:

                unbooked = DoctorSlot.objects.filter(doctor=doctor, date=leave_date_str, is_booked=False)
                deleted_count = unbooked.count()
                unbooked.delete()
                leave_appts = Appointment.objects.filter(doctor=doctor, appointment_date=leave_date_str).exclude(status='CANCELLED')
                cancelled_count = leave_appts.count()
                for appt in leave_appts:
                    appt.status = 'CANCELLED'
                    if appt.payment_status == 'PAID':
                        appt.payment_status = 'REFUNDED'
                    appt.save()
                    if appt.slot:
                        appt.slot.is_booked = False
                        appt.slot.save()

                messages.warning(request, f"Leave registered for {leave_date_str}! Removed {deleted_count} open slots and cancelled/refunded {cancelled_count} bookings.")
            else:
                messages.error(request, "Please select a valid leave date.")

        return redirect('consultations:manage_slots')

    slots = DoctorSlot.objects.filter(doctor=doctor, date__gte=timezone.now().date()).order_by('date', 'start_time')

    context = {
        'doctor': doctor,
        'slots': slots,
    }
    return render(request, 'consultations/manage_slots.html', context)


@login_required
def delete_slot(request, slot_id):
    slot = get_object_or_404(DoctorSlot, id=slot_id)
    if request.user != slot.doctor and not request.user.is_admin:
        messages.error(request, "Unauthorized operation.")
        return redirect('consultations:manage_slots')

    if slot.is_booked:
        messages.error(request, "Cannot delete a time slot that has already been booked by a patient.")
    else:
        slot.delete()
        messages.success(request, "Consultation time slot removed.")

    return redirect('consultations:manage_slots')


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.patient and request.user != appointment.doctor and not request.user.is_admin:
        messages.error(request, "Unauthorized operation to cancel this appointment.")
        return redirect('consultations:my_consultations')

    if appointment.status == 'CANCELLED':
        messages.info(request, "This appointment booking is already cancelled.")
        return redirect('consultations:my_consultations')

    appointment.status = 'CANCELLED'
    if appointment.payment_status == 'PAID':
        appointment.payment_status = 'REFUNDED'
    
    appointment.save()

    if appointment.slot:
        appointment.slot.is_booked = False
        appointment.slot.save()

    messages.success(request, f"Appointment #{appointment.id} has been cancelled successfully. The consultation time slot has been freed up!")

    referer = request.META.get('HTTP_REFERER', '')
    if request.user.is_admin and 'admin-portal' in referer:
        return redirect('accounts:admin_consultations')

    return redirect('consultations:my_consultations')
