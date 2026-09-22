from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def patient_required(view_func):
    """Decorator ensuring only Patient users can access the view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_patient and not request.user.is_superuser:
            messages.error(request, "Access restricted. This page is only available for Patient accounts.")
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def doctor_required(view_func):
    """Decorator ensuring only Doctor users can access the view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_doctor and not request.user.is_superuser:
            messages.error(request, "Access restricted. This page is only available for Doctor accounts.")
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """Decorator ensuring only Admin users can access the view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in with an Admin account to access the Admin Control Portal.")
            return redirect('accounts:admin_login')
        if not request.user.is_admin:
            messages.error(request, "Access restricted. Administrator privileges required.")
            return redirect('dashboard:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
