# spots/models.py
from django.db import models
from django.contrib.auth.models import User  # optional: if you use login

# -----------------------------
# Flight & Seat Models
# -----------------------------
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    business_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField(default=180)

    def __str__(self):
        return f"{self.flight_number} - {self.departure_city} to {self.arrival_city}"

class Seat(models.Model):
    SEAT_CLASSES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
    ]
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)  # e.g., 12A
    seat_class = models.CharField(max_length=10, choices=SEAT_CLASSES)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f"{self.flight.flight_number} - {self.seat_number} ({self.seat_class})"

# -----------------------------
# Passenger & Booking Models
# -----------------------------
class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Booking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    booking_id = models.CharField(max_length=12, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    selected_seats = models.ManyToManyField(Seat)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='confirmed')

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import time
            self.booking_id = f"B{int(time.time())}"  # simple unique ID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.flight.flight_number}"

# -----------------------------
# Flight Search Model
# -----------------------------
class FlightSearch(models.Model):
    TRIP_CHOICES = [
        ('one_way', 'One Way'),
        ('round_trip', 'Round Trip'),
        ('multi', 'Multi-City'),
    ]
    CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
    ]

    trip_type = models.CharField(max_length=20, choices=TRIP_CHOICES)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    infants = models.PositiveIntegerField(default=0)
    flight_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure_date})"
