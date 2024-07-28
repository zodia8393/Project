from django.contrib import admin
from .models import Trip, TripItem

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_date', 'end_date', 'budget')
    list_filter = ('start_date', 'end_date', 'is_public')
    search_fields = ('title', 'user__username', 'user__email')

@admin.register(TripItem)
class TripItemAdmin(admin.ModelAdmin):
    list_display = ('trip', 'destination', 'start_datetime', 'end_datetime')
    list_filter = ('start_datetime', 'end_datetime')
    search_fields = ('trip__title', 'destination__name')