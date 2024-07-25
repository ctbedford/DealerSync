from django.db.models import Count
from scraper.models import VehicleListing

# Find duplicate listings based on certain fields
duplicates = VehicleListing.objects.values(
    'dealership', 'year', 'make', 'model').annotate(count=Count('id')).filter(count__gt=1)

print(f"Number of potential duplicates: {len(duplicates)}")

# Print details of potential duplicates
for dup in duplicates:
    print(f"Potential duplicate: {dup}")
    listings = VehicleListing.objects.filter(
        dealership=dup['dealership'],
        year=dup['year'],
        make=dup['make'],
        model=dup['model']
    )
    for listing in listings:
        print(f"  ID: {listing.id}, Title: {
              listing.title}, Created: {listing.created_at}")
    print()
