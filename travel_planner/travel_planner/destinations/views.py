from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Destination
from .serializers import DestinationSerializer

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['name', 'description', 'country', 'city']
    ordering_fields = ['name', 'country', 'city']