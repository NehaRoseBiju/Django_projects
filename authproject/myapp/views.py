from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request,'login.html')
@login_required
def home(request):
    return render(request,'home.html')
if not User.objects.filter(username='neha').exists():
    User.objects.create_user(
        username='neha',
        password='1234'
    )