from django.urls import path
from . import views

app_name = 'booking'  # ← This creates the namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_flights, name='search_flights'),  # ← ADD THIS
    path('results/', views.search_results, name='search_results'),  # ADD THIS
]
