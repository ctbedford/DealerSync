from django.db import models

class VehicleListing(models.Model):
    dealership = models.CharField(max_length=100)
    title = models.CharField(max_length=500)  # Increased from 200 to 500
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500)  # Increased from default 200 to 500
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - {self.dealership}"
