import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from accounts.models import CustomUser
from wellness.models import JournalEntry, SleepRecord, PhysicalActivity, WaterIntake, Habit
from consultations.models import Appointment
from payments.models import PaymentTransaction

@login_required
def dashboard_index(request):
    user = request.user
    today = timezone.now().date()
    
    if user.is_admin:
        total_patients = CustomUser.objects.filter(role='PATIENT', is_superuser=False, is_staff=False).count()
        total_doctors = CustomUser.objects.filter(role='DOCTOR').count()
        total_admins = CustomUser.objects.filter(Q(role='ADMIN') | Q(is_superuser=True) | Q(is_staff=True)).distinct().count()
        total_users = CustomUser.objects.count()
        
        all_appointments = Appointment.objects.all().order_by('-created_at')
        active_appointments = all_appointments.exclude(status='CANCELLED')
        total_appointments = all_appointments.count()
        completed_appointments = all_appointments.filter(status='COMPLETED').count()
        pending_appointments = all_appointments.filter(status='SCHEDULED').count()

        all_payments = PaymentTransaction.objects.all().order_by('-created_at')
        total_revenue = sum(p.amount for p in all_payments if p.status == 'COMPLETED')
        recent_users = CustomUser.objects.all().order_by('-date_joined')[:6]

        context = {
            'total_users': total_users,
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_admins': total_admins,
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments,
            'pending_appointments': pending_appointments,
            'total_revenue': total_revenue,
            'recent_appointments': active_appointments[:5],
            'recent_payments': all_payments[:5],
            'recent_users': recent_users,
        }
        return render(request, 'dashboard/admin_dashboard.html', context)

    if user.is_doctor:
        upcoming_appointments = Appointment.objects.filter(doctor=user, appointment_date__gte=today, payment_status='PAID').exclude(status='CANCELLED')[:5]
        total_consultations = Appointment.objects.filter(doctor=user, payment_status='PAID').exclude(status='CANCELLED').count()
        payments = PaymentTransaction.objects.filter(doctor=user, status='COMPLETED')
        total_earnings = sum(p.amount for p in payments)
        
        context = {
            'upcoming_appointments': upcoming_appointments,
            'total_consultations': total_consultations,
            'total_earnings': total_earnings,
            'recent_payments': payments[:5],
        }
        return render(request, 'dashboard/doctor_dashboard.html', context)


    water, _ = WaterIntake.objects.get_or_create(user=user, date=today)

    upcoming_appointments = Appointment.objects.filter(patient=user, appointment_date__gte=today).exclude(status='CANCELLED')[:3]

    habits = Habit.objects.filter(user=user)

    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    day_labels = [d.strftime('%a') for d in last_7_days]
    sleep_records = {s.date: float(s.duration_hours) for s in SleepRecord.objects.filter(user=user, date__gte=today - timedelta(days=7))}
    sleep_data = [sleep_records.get(d, 0.0) for d in last_7_days]

    activities = PhysicalActivity.objects.filter(user=user, date__gte=today - timedelta(days=7))
    activity_map = {}
    for act in activities:
        activity_map[act.date] = activity_map.get(act.date, 0) + act.calories_burned
    activity_data = [activity_map.get(d, 0) for d in last_7_days]

    journals = JournalEntry.objects.filter(user=user)
    mood_counts = {
        'GREAT': journals.filter(mood='GREAT').count(),
        'GOOD': journals.filter(mood='GOOD').count(),
        'CALM': journals.filter(mood='CALM').count(),
        'ANXIOUS': journals.filter(mood='ANXIOUS').count(),
        'TIRED': journals.filter(mood='TIRED').count(),
        'SAD': journals.filter(mood='SAD').count(),
    }

    quotes = [
        "Small daily habits create extraordinary long-term health.",
        "Your mind and body are an interconnected ecosystem. Nurture both.",
        "Sleep is the foundation of peak biological performance.",
        "Hydration increases mental clarity and energy flow."
    ]
    motivation = quotes[hash(str(today)) % len(quotes)]

    context = {
        'water': water,
        'upcoming_appointments': upcoming_appointments,
        'habits': habits,
        'motivation': motivation,
        'day_labels_json': json.dumps(day_labels),
        'sleep_data_json': json.dumps(sleep_data),
        'activity_data_json': json.dumps(activity_data),
        'mood_counts_json': json.dumps(list(mood_counts.values())),
        'recent_journals': journals[:3],
    }
    return render(request, 'dashboard/patient_dashboard.html', context)
