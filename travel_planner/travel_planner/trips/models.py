from django.db import models
from django.conf import settings
from travel_planner.destinations.models import Destination

class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s trip: {self.title}"

class TripItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='items')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.trip.title} - {self.destination.name}"