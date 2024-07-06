from django.core.management.base import BaseCommand
from scraper.models import VehicleListing

class Command(BaseCommand):
    help = 'Check the content of the VehicleListing table'

    def handle(self, *args, **options):
        total_listings = VehicleListing.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total vehicle listings: {total_listings}'))

        if total_listings > 0:
            latest_listings = VehicleListing.objects.order_by('-created_at')[:5]
            self.stdout.write(self.style.SUCCESS('Latest 5 listings:'))
            for listing in latest_listings:
                self.stdout.write(f'{listing.year} {listing.make} {listing.model} - ${listing.price}')
        else:
            self.stdout.write(self.style.WARNING('No listings found in the database.'))
