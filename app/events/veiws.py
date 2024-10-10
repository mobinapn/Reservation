from django.shortcuts import render
from django.utils import timezone
from .models import Event
from django.db.models import Q

# Combined view to display events and apply filters
def event_list(request):
    events = Event.objects.all()

    # Get filter parameters from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    place = request.GET.get('place')
    min_capacity = request.GET.get('min_capacity')
    max_capacity = request.GET.get('max_capacity')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Apply filters
    if start_date and end_date:
        events = events.filter(begin_date__gte=start_date, end_date__lte=end_date)
    
    if place:
        events = events.filter(place__icontains=place)
    
    if min_capacity and max_capacity:
        events = events.filter(capacity__gte=int(min_capacity), capacity__lte=int(max_capacity))
    
    if min_rate and max_rate:
        events = events.filter(rate__gte=float(min_rate), rate__lte=float(max_rate))
    
    if min_price and max_price:
        events = events.filter(price__gte=float(min_price), price__lte=float(max_price))

    # Render the index.html template with filtered events
    return render(request, 'events/index.html', {'events': events})
