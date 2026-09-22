from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:appointment_id>/', views.checkout_view, name='checkout'),
    path('receipt/<str:transaction_id>/', views.view_receipt, name='receipt'),
    path('history/', views.payment_history, name='history'),
]
