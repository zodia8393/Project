from celery import shared_task
from django.core.mail import send_mail
from .models import Trip
from datetime import date, timedelta

@shared_task
def send_trip_reminder():
    tomorrow = date.today() + timedelta(days=1)
    trips = Trip.objects.filter(start_date=tomorrow)
    for trip in trips:
        send_mail(
            'Trip Reminder',
            f'Your trip "{trip.title}" starts tomorrow!',
            'noreply@travelplanner.com',
            [trip.user.email],
            fail_silently=False,
        )