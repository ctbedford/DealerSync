from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class VehicleListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicle_listings')
    # ... rest of the model fields ...)
    dealership = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    needs_update = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.dealership} (User: {self.user.username})"


class SyncAttempt(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sync_attempts', null=True, blank=True )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    listings_added = models.IntegerField(default=0)
    listings_updated = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sync Attempt {self.id} - {self.status} (User: {self.user.username})"

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return timezone.now() - self.start_time
