from rest_framework import serializers
from .models import Destination, Attraction

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    attractions = AttractionSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = '__all__'