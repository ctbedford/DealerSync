from django.contrib import admin
from .models import VehicleListing

@admin.register(VehicleListing)
class VehicleListingAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'price', 'msrp', 'dealership')
    list_filter = ('make', 'year', 'dealership')
    search_fields = ('make', 'model', 'dealership')

