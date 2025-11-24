# main/admin.py
from django.contrib import admin
from .models import FlightSearch

@admin.register(FlightSearch)
class FlightSearchAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'departure_date', 'trip_type', 'flight_class', 'created_at')