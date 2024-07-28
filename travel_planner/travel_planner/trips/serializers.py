from rest_framework import serializers
from .models import Trip, TripItem

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('user',)

class TripItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripItem
        fields = '__all__'
        read_only_fields = ('trip',)