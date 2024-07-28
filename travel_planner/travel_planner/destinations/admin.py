from django.contrib import admin
from .models import Destination, Attraction

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'city', 'country')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination')
    list_filter = ('destination__country',)
    search_fields = ('name', 'destination__name')