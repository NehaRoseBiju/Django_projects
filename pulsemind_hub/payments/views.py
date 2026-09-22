import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from consultations.models import Appointment
from .models import PaymentTransaction

@login_required
def checkout_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if appointment.payment_status == 'PAID':
        messages.success(request, "This appointment has already been paid for!")
        return redirect('consultations:video_room', room_id=appointment.meeting_room_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'CARD')
        
        # Process & confirm payment
        transaction = PaymentTransaction.objects.create(
            appointment=appointment,
            patient=request.user,
            doctor=appointment.doctor,
            amount=appointment.fee,
            transaction_id=f"PAY-{uuid.uuid4().hex[:10].upper()}",
            payment_method=payment_method,
            status='COMPLETED'
        )

        # Update appointment payment status and mark slot as booked
        appointment.payment_status = 'PAID'
        appointment.save()

        if appointment.slot:
            appointment.slot.is_booked = True
            appointment.slot.save()

        messages.success(request, "Payment successful! Your consultation is now confirmed.")
        return redirect('payments:receipt', transaction_id=transaction.transaction_id)

    context = {
        'appointment': appointment,
        'doctor': appointment.doctor,
        'fee': appointment.fee,
    }
    return render(request, 'payments/checkout.html', context)


@login_required
def view_receipt(request, transaction_id):
    transaction = get_object_or_404(PaymentTransaction, transaction_id=transaction_id)
    
    # Check authorization
    if request.user != transaction.patient and request.user != transaction.doctor:
        messages.error(request, "Unauthorized access to transaction receipt.")
        return redirect('dashboard:index')

    context = {
        'transaction': transaction,
        'appointment': transaction.appointment,
        'patient': transaction.patient,
        'doctor': transaction.doctor,
    }
    return render(request, 'payments/receipt.html', context)


@login_required
def payment_history(request):
    if request.user.is_doctor:
        payments = PaymentTransaction.objects.filter(doctor=request.user)
    else:
        payments = PaymentTransaction.objects.filter(patient=request.user)

    return render(request, 'payments/history.html', {'payments': payments})
