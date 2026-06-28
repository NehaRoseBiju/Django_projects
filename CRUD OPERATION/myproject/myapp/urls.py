from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Course URLs
    path('course/', views.course_list, name='course_list'),
    path('course/add/', views.course_create, name='course_create'),
    path('course/update/<int:id>/', views.course_update, name='course_update'),
    path('course/delete/<int:id>/', views.course_delete, name='course_delete'),

    # Instructor URLs
    path('instructor/', views.instructor_list, name='instructor_list'),
    path('instructor/add/', views.instructor_create, name='instructor_create'),
    path('instructor/update/<int:id>/', views.instructor_update, name='instructor_update'),
    path('instructor/delete/<int:id>/', views.instructor_delete, name='instructor_delete'),

]