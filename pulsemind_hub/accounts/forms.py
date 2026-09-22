from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Public registration form for Patients.
    Doctor registration is strictly managed by Admins via Django Admin.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (+91)'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'PATIENT'  # Public self-registration is strictly for Patients
        if commit:
            user.save()
        return user


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'wellness_goal', 'emergency_contact_name', 'emergency_contact_phone', 'bio')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'wellness_goal': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'specialization', 'qualification', 'experience_years', 'consultation_fee', 'bio')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AdminUserManageForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to keep existing password'}), required=False, help_text="Only enter if you wish to change/reset password")

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'phone', 'role', 
            'is_active', 'is_staff', 'is_superuser',
            'specialization', 'qualification', 'consultation_fee', 'experience_years', 'bio'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select', 'id': 'id_role_select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Cardiologist'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MBBS, MD'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '50'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        new_pw = self.cleaned_data.get('new_password')
        if new_pw:
            user.set_password(new_pw)
        if commit:
            user.save()
        return user
