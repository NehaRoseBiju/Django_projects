from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Flight
from .models import Booking

def flight_list(request):
    flights = Flight.objects.all()
    return render(request,'flight_list.html',{'flights':flights})

def add_flight(request):
    if request.method == 'POST':
        Flight.objects.create(
            flight_no=request.POST['flight_no'],
            source=request.POST['source'],
            destination=request.POST['destination'],
            departure_date=request.POST['departure_date'],
            departure_time=request.POST['departure_time'],
            price=request.POST['price'],
            seats=request.POST['seats']
        )
        return redirect('flight_list')
    return render(request,'flight_form.html')

def update_flight(request, id):
    flight = get_object_or_404(Flight, id=id)
    if request.method == "POST":
        flight.flight_no = request.POST["flight_no"]
        flight.source = request.POST["source"]
        flight.destination = request.POST["destination"]
        flight.departure_date = request.POST["departure_date"]
        flight.departure_time = request.POST["departure_time"]
        flight.price = request.POST["price"]
        flight.seats = request.POST["seats"]
        flight.save()
        return redirect("flight_list")
    return render(request, "update.html", {"flight": flight})

def delete_flight(request,id):
    flight = Flight.objects.get(id=id)
    flight.delete()
    return redirect('flight_list')


def search_flight(request):
    flights = Flight.objects.all()
    source = request.GET.get('source')
    destination = request.GET.get(
        'destination'
    )
    if source:
        flights = flights.filter(
            source__icontains=source
        )
    if destination:
        flights = flights.filter(
            destination__icontains=destination
        )
    return render(
        request,
        'search.html',
        {'flights':flights}
    )

def book_flight(request,id):
    flight = Flight.objects.get(id=id)
    if request.method == 'POST':
        Booking.objects.create(
            passenger_name=
            request.POST['name'],
            passenger_email=
            request.POST['email'],
            flight=flight
        )
        return redirect('flight_list')
    return render(
        request,
        'booking.html',
        {'flight':flight}
    )