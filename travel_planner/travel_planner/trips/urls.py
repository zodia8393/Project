from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripViewSet, TripItemViewSet

router = DefaultRouter()
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'trips/(?P<trip_pk>\d+)/items', TripItemViewSet, basename='trip-item')

urlpatterns = [
    path('', include(router.urls)),
]