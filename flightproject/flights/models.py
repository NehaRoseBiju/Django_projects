from django.db import models
class Flight(models.Model):
    flight_no = models.CharField(max_length=20)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price = models.IntegerField()
    seats = models.IntegerField()
    def __str__(self):
        return self.flight_no

class Booking(models.Model):
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.passenger_name