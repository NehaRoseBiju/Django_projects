from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, PatientProfileForm, DoctorProfileForm, AdminUserManageForm
from .models import CustomUser
from .decorators import admin_required
from consultations.models import Appointment
from payments.models import PaymentTransaction

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to PulseMind Hub, {user.username}!")
            return redirect('dashboard:index')
        else:
            messages.error(request, "Registration failed. Please check the details entered.")
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as {user.username}")
            return redirect('dashboard:index')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'accounts/login.html')


def admin_login_view(request):
    if request.user.is_authenticated:
        if getattr(request.user, 'is_admin', False):
            return redirect('dashboard:index')
        else:
            logout(request)

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)

        if user is not None:
            if getattr(user, 'is_admin', False):
                login(request, user)
                messages.success(request, f"Welcome to the PulseMind Hub Admin Portal, {user.username}!")
                return redirect('dashboard:index')
            else:
                messages.error(request, "Access Denied: Standard user accounts (Patients/Doctors) cannot access the Admin Portal.")
        else:
            messages.error(request, "Invalid admin username or password.")

    return render(request, 'accounts/admin_login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    user = request.user
    is_doc = getattr(user, 'is_doctor', False)
    if request.method == 'POST':
        if is_doc:
            form = DoctorProfileForm(request.POST, instance=user)
        else:
            form = PatientProfileForm(request.POST, instance=user)
            
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile')
    else:
        if is_doc:
            form = DoctorProfileForm(instance=user)
        else:
            form = PatientProfileForm(instance=user)
            
    return render(request, 'accounts/profile.html', {'form': form, 'user': user})


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, f"Password reset instructions have been sent to {email}.")
        return redirect('accounts:login')
    return render(request, 'accounts/password_reset.html')


@admin_required
def admin_user_list(request):
    role_filter = request.GET.get('role', 'ALL').strip().upper()
    status_filter = request.GET.get('status', 'ALL').strip().lower()
    search_query = request.GET.get('q', '').strip()

    users = CustomUser.objects.all().order_by('-date_joined')

    if role_filter == 'PATIENT':
        users = users.filter(role='PATIENT', is_superuser=False, is_staff=False)
    elif role_filter == 'DOCTOR':
        users = users.filter(role='DOCTOR')
    elif role_filter == 'ADMIN':
        users = users.filter(Q(role='ADMIN') | Q(is_superuser=True) | Q(is_staff=True))

    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )


    total_users_count = CustomUser.objects.count()
    patients_count = CustomUser.objects.filter(role='PATIENT', is_superuser=False, is_staff=False).count()
    doctors_count = CustomUser.objects.filter(role='DOCTOR').count()
    admins_count = CustomUser.objects.filter(Q(role='ADMIN') | Q(is_superuser=True) | Q(is_staff=True)).distinct().count()

    context = {
        'users': users,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_users_count': total_users_count,
        'patients_count': patients_count,
        'doctors_count': doctors_count,
        'admins_count': admins_count,
    }
    return render(request, 'accounts/admin_user_list.html', context)


@admin_required
def admin_user_add(request):
    """Add a new user (Patient, Doctor, or Admin) directly from Admin Portal."""
    if request.method == 'POST':
        form = AdminUserManageForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User account for '{user.username}' created successfully as {user.get_role_display()}!")
            return redirect('accounts:admin_user_list')
        else:
            messages.error(request, "Error creating user account. Please check the form errors below.")
    else:
        form = AdminUserManageForm()

    return render(request, 'accounts/admin_user_form.html', {'form': form, 'is_edit': False})


@admin_required
def admin_user_edit(request, user_id):

    target_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = AdminUserManageForm(request.POST, instance=target_user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User '{user.username}' details updated successfully!")
            return redirect('accounts:admin_user_list')
        else:
            messages.error(request, "Error updating user details. Please review form inputs.")
    else:
        form = AdminUserManageForm(instance=target_user)

    return render(request, 'accounts/admin_user_form.html', {'form': form, 'target_user': target_user, 'is_edit': True})


@admin_required
def admin_user_toggle_status(request, user_id):

    target_user = get_object_or_404(CustomUser, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot suspend your own active administrator account!")
        return redirect('accounts:admin_user_list')

    target_user.is_active = not target_user.is_active
    target_user.save()

    status_str = "activated" if target_user.is_active else "suspended"
    messages.info(request, f"User account '{target_user.username}' has been {status_str}.")
    return redirect('accounts:admin_user_list')


@admin_required
def admin_user_delete(request, user_id):

    target_user = get_object_or_404(CustomUser, id=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own active administrator account!")
        return redirect('accounts:admin_user_list')

    username = target_user.username
    target_user.delete()
    messages.success(request, f"User '{username}' was permanently removed from the system.")
    return redirect('accounts:admin_user_list')


@admin_required
def admin_consultations(request):

    status_filter = request.GET.get('status', 'ALL')
    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')

    if status_filter != 'ALL':
        appointments = appointments.filter(status=status_filter)

    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'accounts/admin_consultations.html', context)


@admin_required
def admin_payments(request):

    payments = PaymentTransaction.objects.all().order_by('-created_at')
    total_revenue = sum(p.amount for p in payments if p.status == 'COMPLETED')

    context = {
        'payments': payments,
        'total_revenue': total_revenue,
    }
    return render(request, 'accounts/admin_payments.html', context)

