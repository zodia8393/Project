from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Destination

class DestinationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.destination_data = {
            'name': 'Test Destination',
            'country': 'Test Country',
            'city': 'Test City'
        }
        Destination.objects.create(**self.destination_data)

    def test_get_destinations(self):
        response = self.client.get('/api/destinations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_destinations(self):
        response = self.client.get('/api/destinations/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Destination')