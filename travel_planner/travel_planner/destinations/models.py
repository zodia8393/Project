from django.db import models
from django.utils.translation import gettext_lazy as _

class Destination(models.Model):
    name = models.CharField(_('name'), max_length=255)
    country = models.CharField(_('country'), max_length=255)
    city = models.CharField(_('city'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(_('image'), upload_to='destinations/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"

class Attraction(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='attractions')
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    address = models.CharField(_('address'), max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.name} in {self.destination.name}"