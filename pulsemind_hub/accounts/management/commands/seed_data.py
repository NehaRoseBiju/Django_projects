import uuid
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser
from wellness.models import JournalEntry, SleepRecord, PhysicalActivity, WaterIntake, Habit
from consultations.models import DoctorSlot, Appointment
from payments.models import PaymentTransaction

class Command(BaseCommand):
    help = 'Seeds database with realistic initial Indian doctors, slots, patient, wellness entries, and demo video room appointment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding PulseMind Hub database with Indian health context..."))

        # 0. Create Admin Superuser for Platform Management
        admin_user, admin_created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pulsemind.in',
                'first_name': 'Platform',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
                'role': 'ADMIN'
            }
        )
        admin_user.role = 'ADMIN'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('Admin123!')
        admin_user.save()
        self.stdout.write(self.style.SUCCESS("Created Admin Superuser: admin (Password: Admin123!)"))

        # 1. Create Patient
        patient, created = CustomUser.objects.get_or_create(
            username='patient_john',
            defaults={
                'email': 'john.sharma@pulsemind.in',
                'first_name': 'John',
                'last_name': 'Sharma',
                'role': 'PATIENT',
                'wellness_goal': 'Consistent sleep, 3L hydration, and Yoga',
                'phone': '+91 98765 43210'
            }
        )
        if created or patient:
            patient.first_name = 'John'
            patient.last_name = 'Sharma'
            patient.set_password('Password123!')
            patient.save()
            self.stdout.write(self.style.SUCCESS("Updated Patient: John Sharma (patient_john / Password123!)"))

        # 2. Create Doctors with Indian Qualifications & Fees in ₹
        doctors_data = [
            {
                'username': 'dr_sarah',
                'first_name': 'Sarah',
                'last_name': 'Jenkins',
                'email': 'sarah.jenkins@pulsemind.in',
                'specialization': 'Cardiology & Heart Care',
                'qualification': 'MBBS, MD Cardiology (AIIMS New Delhi)',
                'consultation_fee': 650.00,
                'experience_years': 12,
                'bio': 'Senior Cardiologist specializing in preventive heart health and lifestyle medical guidance.'
            },
            {
                'username': 'dr_alex',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'email': 'alex.rivera@pulsemind.in',
                'specialization': 'Psychiatry & Mental Wellness',
                'qualification': 'MD Psychiatry (NIMHANS Bengaluru)',
                'consultation_fee': 800.00,
                'experience_years': 10,
                'bio': 'Compassionate psychiatrist focused on stress reduction, anxiety management, and cognitive therapy.'
            },
            {
                'username': 'dr_emily',
                'first_name': 'Emily',
                'last_name': 'Chen',
                'email': 'emily.chen@pulsemind.in',
                'specialization': 'Neurology & Sleep Medicine',
                'qualification': 'MBBS, DM Neurology (PGIMER Chandigarh)',
                'consultation_fee': 750.00,
                'experience_years': 8,
                'bio': 'Neurologist expert in sleep architecture, insomnia recovery, and brain wellness.'
            },
            {
                'username': 'dr_michael',
                'first_name': 'Michael',
                'last_name': 'Vance',
                'email': 'michael.vance@pulsemind.in',
                'specialization': 'General Medicine & Wellness',
                'qualification': 'MBBS, DNB Internal Medicine',
                'consultation_fee': 500.00,
                'experience_years': 15,
                'bio': 'Primary physician focusing on general health checkups, preventative care, and diet consultation.'
            }
        ]

        created_doctors = []
        for doc_info in doctors_data:
            doc, d_created = CustomUser.objects.get_or_create(
                username=doc_info['username'],
                defaults={
                    'role': 'DOCTOR',
                    'email': doc_info['email'],
                    'first_name': doc_info['first_name'],
                    'last_name': doc_info['last_name'],
                    'specialization': doc_info['specialization'],
                    'qualification': doc_info['qualification'],
                    'consultation_fee': doc_info['consultation_fee'],
                    'experience_years': doc_info['experience_years'],
                    'bio': doc_info['bio']
                }
            )
            # Ensure fee & details updated to Indian Rupees
            doc.consultation_fee = doc_info['consultation_fee']
            doc.qualification = doc_info['qualification']
            doc.specialization = doc_info['specialization']
            doc.set_password('Password123!')
            doc.save()
            created_doctors.append(doc)

        # 3. Create Slots
        today = timezone.now().date()
        for doc in created_doctors:
            for i in range(1, 4):
                slot_date = today + timedelta(days=i)
                DoctorSlot.objects.get_or_create(
                    doctor=doc,
                    date=slot_date,
                    start_time=timezone.datetime.strptime("10:00", "%H:%M").time(),
                    end_time=timezone.datetime.strptime("10:30", "%H:%M").time()
                )
                DoctorSlot.objects.get_or_create(
                    doctor=doc,
                    date=slot_date,
                    start_time=timezone.datetime.strptime("14:30", "%H:%M").time(),
                    end_time=timezone.datetime.strptime("15:00", "%H:%M").time()
                )

        # 4. Create Demo Appointment & Paid Payment Transaction for Video Call testing
        doc_sarah = created_doctors[0]
        demo_room_id = "demo-consultation-room-101"
        
        appt, appt_created = Appointment.objects.get_or_create(
            meeting_room_id=demo_room_id,
            defaults={
                'patient': patient,
                'doctor': doc_sarah,
                'appointment_date': today,
                'appointment_time': timezone.datetime.strptime("11:00", "%H:%M").time(),
                'symptoms_notes': 'Routine cardiac checkup & discussion on morning yoga heart rate readings.',
                'fee': doc_sarah.consultation_fee,
                'status': 'SCHEDULED',
                'payment_status': 'PAID'
            }
        )
        if not appt_created:
            appt.fee = doc_sarah.consultation_fee
            appt.payment_status = 'PAID'
            appt.save()

        # Payment Transaction in Rupees
        payment, p_created = PaymentTransaction.objects.get_or_create(
            appointment=appt,
            defaults={
                'patient': patient,
                'doctor': doc_sarah,
                'amount': doc_sarah.consultation_fee,
                'transaction_id': f"PAY-IND-{uuid.uuid4().hex[:6].upper()}",
                'payment_method': 'UPI',
                'status': 'COMPLETED'
            }
        )
        if not p_created:
            payment.amount = doc_sarah.consultation_fee
            payment.payment_method = 'UPI'
            payment.save()

        # 5. Create Wellness Data for Patient
        WaterIntake.objects.get_or_create(user=patient, date=today, defaults={'glasses_logged': 6, 'goal_glasses': 8})
        
        Habit.objects.get_or_create(user=patient, title='15 Min Morning Yoga & Pranayama', defaults={'frequency': 'DAILY', 'streak_count': 5, 'is_completed_today': True, 'last_completed_date': today})
        Habit.objects.get_or_create(user=patient, title='Drink 2.5L Water Daily', defaults={'frequency': 'DAILY', 'streak_count': 7, 'is_completed_today': True, 'last_completed_date': today})
        Habit.objects.get_or_create(user=patient, title='No Mobile 30 Min Before Bed', defaults={'frequency': 'DAILY', 'streak_count': 3, 'is_completed_today': False})

        # Past 5 days sleep & activity data for Chart.js graphs
        sample_sleeps = [7.5, 8.0, 6.5, 7.0, 8.2]
        sample_cals = [320, 450, 280, 500, 380]
        sample_exercises = ['Morning Walk', 'Surya Namaskar & Yoga', 'Brisk Cycling', 'Evening Walk', 'Strength Training']

        for idx in range(5):
            past_date = today - timedelta(days=idx)
            SleepRecord.objects.get_or_create(
                user=patient,
                date=past_date,
                defaults={
                    'bedtime': timezone.datetime.strptime("22:30", "%H:%M").time(),
                    'wake_time': timezone.datetime.strptime("06:30", "%H:%M").time(),
                    'duration_hours': sample_sleeps[idx],
                    'quality_rating': 4,
                    'disturbances': 'slept peacefully'
                }
            )
            PhysicalActivity.objects.get_or_create(
                user=patient,
                date=past_date,
                exercise_type=sample_exercises[idx],
                defaults={
                    'duration_minutes': 40,
                    'intensity': 'MODERATE',
                    'calories_burned': sample_cals[idx]
                }
            )

        JournalEntry.objects.get_or_create(
            user=patient,
            date=today,
            defaults={
                'mood': 'GREAT',
                'content': 'Feeling energized today after morning Yoga and peaceful rest!'
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully re-seeded database with Indian terms and INR Rupee prices!"))
