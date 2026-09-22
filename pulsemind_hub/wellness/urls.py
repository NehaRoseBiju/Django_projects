from django.urls import path
from . import views

app_name = 'wellness'

urlpatterns = [
    path('', views.wellness_index, name='index'),
    path('journal/add/', views.add_journal, name='add_journal'),
    path('sleep/add/', views.add_sleep, name='add_sleep'),
    path('activity/add/', views.add_activity, name='add_activity'),
    path('water/log/', views.log_water, name='log_water'),
    path('habit/add/', views.add_habit, name='add_habit'),
    path('habit/toggle/<int:habit_id>/', views.toggle_habit, name='toggle_habit'),
]
