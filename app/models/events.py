from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import TourOrganizer  # Import the existing TourOrganizer model

class Event(models.Model):
    # Fields
    cover_photo = models.ImageField(upload_to='event_covers/', blank=True, null=True)  # Cover photo
    details = models.TextField()  # Event details
    begin_date = models.DateTimeField()  # Start of the event
    end_date = models.DateTimeField()  # End of the event
    rate = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])  # Rating between 0 and 5
    comments = models.TextField(blank=True, null=True)  # Comments section (optional)
    place = models.CharField(max_length=255)  # Place of the event
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])  # Event price
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # Capacity of the event
    
    # Relationships
    organizer = models.ForeignKey(TourOrganizer, on_delete=models.CASCADE, related_name="events")  # Event organizer from accounts app
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)  # When the event was created
    updated_at = models.DateTimeField(auto_now=True)  # When the event was last updated

    def __str__(self):
        return f"{self.place} - {self.begin_date.strftime('%Y-%m-%d')}"

    def is_upcoming(self):
        """Check if the event is in the future."""
        return self.begin_date > timezone.now()

    def is_ongoing(self):
        """Check if the event is currently happening."""
        return self.begin_date <= timezone.now() <= self.end_date


class EventPhoto(models.Model):
    # Fields for event photos
    event = models.ForeignKey(Event, related_name='tour_place_photos', on_delete=models.CASCADE)  # Link to the event
    photo = models.ImageField(upload_to='event_tour_photos/')  # Photo of the tour place
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description of the photo
    
    def __str__(self):
        return f"Photo for {self.event.place}"
