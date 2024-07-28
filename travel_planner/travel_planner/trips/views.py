from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Trip, TripItem
from .serializers import TripSerializer, TripItemSerializer

class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TripItemViewSet(viewsets.ModelViewSet):
    serializer_class = TripItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TripItem.objects.filter(trip__user=self.request.user)

    def perform_create(self, serializer):
        trip = Trip.objects.get(id=self.kwargs['trip_pk'], user=self.request.user)
        serializer.save(trip=trip)