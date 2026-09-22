from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'specialization', 'consultation_fee', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Medical Practice Info (Admin Only)', {
            'fields': ('role', 'specialization', 'qualification', 'consultation_fee', 'experience_years', 'wellness_goal', 'phone', 'bio')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Selection', {
            'fields': ('role', 'specialization', 'qualification', 'consultation_fee', 'experience_years', 'phone')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
