from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# ---------------------------
# Home and static pages
# ---------------------------
def home(request):
    return render(request, 'home.html')


def places(request):
    return render(request, 'places.html')


def contact(request):
    return render(request, 'contact.html')


# ---------------------------
# Step 1: Flight Search
# ---------------------------
def search_flights(request):
    if request.method == 'POST':
        origin = request.POST.get('origin', '').strip()
        destination = request.POST.get('destination', '').strip()
        departure_date = request.POST.get('departure_date', '').strip()
        return_date = request.POST.get('return_date', '').strip()

        # Basic validation
        if not origin or not destination or not departure_date:
            messages.error(request, "Please provide origin, destination, and departure date.")
            return render(request, "main/search_form.html")

        # Save search data in session
        booking_data = {
            'from_location': origin,
            'to_location': destination,
            'departure_date': departure_date,
            'return_date': return_date,
            'adults': request.POST.get('adults', '1'),
            'children': request.POST.get('children', '0'),
            'infants': request.POST.get('infants', '0'),
            'flight_class': request.POST.get('flight_class', 'economy'),
        }
        request.session['booking_data'] = booking_data
        return redirect('booking:search_results')  # ✅ Namespace added

    return render(request, "main/search_form.html")


# ---------------------------
# Step 2: Show Search Results
# ---------------------------
def search_results(request):
    booking = request.session.get('booking_data')
    if not booking:
        messages.warning(request, "No search data found. Please start a new search.")
        return redirect('booking:search_flights')  # ✅ Namespace added

    # Mock flight data (replace with DB queries if needed)
    flights = [
        {
            'origin': booking['from_location'],
            'destination': f"{booking['to_location']} (LHR)",
            'departure_date': booking['departure_date'],
            'price': 550,
            'airline': 'Indigo Airways'
        },
        {
            'origin': booking['from_location'],
            'destination': f"{booking['to_location']} (CDG)",
            'departure_date': booking['departure_date'],
            'price': 620,
            'airline': 'Jet Airways'
        }
    ]
    return render(request, 'main/search_results.html', {
        'flights': flights,
        'booking': booking
    })


# ---------------------------
# Step 3: Seat Selection
# ---------------------------
def select_seats(request):
    booking = request.session.get('booking_data')
    if not booking:
        messages.warning(request, "Booking session expired. Please search again.")
        return redirect('booking:search_flights')  # ✅ Namespace added

    return render(request, 'main/select_seats.html', {'booking': booking})


# ---------------------------
# Step 4: Confirm Booking
# ---------------------------
def confirm_booking(request):
    if request.method == 'POST':
        booking = request.session.get('booking_data')
        if not booking:
            messages.error(request, "Booking data not found. Please start over.")
            return redirect('booking:search_flights')  # ✅ Namespace added

        selected_seats = request.POST.get('selected_seats', '').strip()
        context = {
            'booking': booking,
            'seats': selected_seats
        }
        return render(request, 'navbar/confirmation.html', context)

    # GET requests: prevent direct access
    messages.warning(request, "Access denied. Please follow the booking steps.")
    return redirect('booking:search_flights')  # ✅ Namespace added


# ---------------------------
# User login
# ---------------------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')
