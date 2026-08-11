from django.urls import path
from . import views

urlpatterns = [
    path('',views.flight_list,name='flight_list'),
    path('add/',views.add_flight,name='add_flight'),
    path('update/<int:id>/',views.update_flight,name='update_flight'),
    path('delete/<int:id>/',views.delete_flight,name='delete_flight'),
    path('search/',views.search_flight,name='search_flight'),
    path('book/<int:id>/',views.book_flight,name='book_flight'),
]