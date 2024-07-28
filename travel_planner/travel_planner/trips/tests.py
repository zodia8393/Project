from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Trip
from datetime import date

User = get_user_model()

class TripTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.trip_data = {
            'title': 'Test Trip',
            'start_date': date.today(),
            'end_date': date.today(),
            'budget': '1000.00'
        }

    def test_create_trip(self):
        response = self.client.post('/api/trips/', self.trip_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.count(), 1)
        self.assertEqual(Trip.objects.get().title, 'Test Trip')

    def test_get_trips(self):
        Trip.objects.create(user=self.user, **self.trip_data)
        response = self.client.get('/api/trips/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)