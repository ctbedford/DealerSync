from rest_framework import serializers
from .models import VehicleListing


class VehicleListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleListing
        fields = ['id', 'dealership', 'title', 'price', 'msrp', 'year', 'make',
                  'model', 'image_url', 'created_at', 'updated_at', 'views', 'needs_update']
        read_only_fields = ['id', 'created_at', 'updated_at', 'views']
