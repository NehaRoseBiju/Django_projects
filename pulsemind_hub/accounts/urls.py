from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    
    # Admin Portal Management Routes
    path('admin-portal/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-portal/users/add/', views.admin_user_add, name='admin_user_add'),
    path('admin-portal/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-portal/users/<int:user_id>/toggle-status/', views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('admin-portal/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-portal/consultations/', views.admin_consultations, name='admin_consultations'),
    path('admin-portal/payments/', views.admin_payments, name='admin_payments'),
]
