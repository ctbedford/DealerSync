from django.db import models

class VehicleListing(models.Model):
    dealership = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    exterior_color = models.CharField(max_length=50)
    interior_color = models.CharField(max_length=50)
    mileage = models.IntegerField()
    fuel_economy = models.CharField(max_length=100)
    transmission = models.CharField(max_length=50)
    engine = models.CharField(max_length=100)
    vin = models.CharField(max_length=17)
    stock_number = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.URLField()
    listing_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.dealership}"
