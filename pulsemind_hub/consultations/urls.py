from django.urls import path
from . import views

app_name = 'consultations'

urlpatterns = [
    path('doctors/', views.doctor_directory, name='doctors'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book'),
    path('room/<str:room_id>/', views.video_room, name='video_room'),
    path('my-consultations/', views.my_consultations, name='my_consultations'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('slots/', views.manage_slots, name='manage_slots'),
    path('slots/<int:slot_id>/delete/', views.delete_slot, name='delete_slot'),
]
