from django.contrib import admin
from .models import VehicleListing, SyncAttempt

@admin.register(VehicleListing)
class VehicleListingAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'price', 'msrp', 'dealership', 'views', 'needs_update')
    list_filter = ('make', 'year', 'dealership', 'needs_update')
    search_fields = ('make', 'model', 'dealership')

@admin.register(SyncAttempt)
class SyncAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status', 'listings_added', 'listings_updated')
    list_filter = ('status',)
    readonly_fields = ('start_time', 'end_time', 'duration')
