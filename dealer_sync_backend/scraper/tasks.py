from celery import shared_task
from .scraper import scrape_mclarty_daniel
from .models import SyncAttempt, VehicleListing
from django.contrib.auth import get_user_model
from django.utils import timezone

@shared_task
def run_scrapers(user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        sync_attempt = SyncAttempt.objects.create(user=user, status='IN_PROGRESS')
        
        listings = scrape_mclarty_daniel()
        listings_added = 0
        listings_updated = 0
        
        for listing_data in listings:
            listing, created = VehicleListing.objects.update_or_create(
                user=user,
                dealership=listing_data['dealership'],
                title=listing_data['title'],
                defaults={
                    'price': listing_data.get('price'),
                    'msrp': listing_data.get('msrp'),
                    'year': listing_data['year'],
                    'make': listing_data['make'],
                    'model': listing_data['model'],
                    'image_url': listing_data.get('image_url'),
                    'needs_update': False
                }
            )
            
            if created:
                listings_added += 1
            else:
                listings_updated += 1
        
        sync_attempt.status = 'COMPLETED'
        sync_attempt.listings_added = listings_added
        sync_attempt.listings_updated = listings_updated
        sync_attempt.end_time = timezone.now()
        sync_attempt.save()
        
        return f"Scraping completed successfully. Added: {listings_added}, Updated: {listings_updated}"
    
    except Exception as e:
        if 'sync_attempt' in locals():
            sync_attempt.status = 'FAILED'
            sync_attempt.error_message = str(e)
            sync_attempt.end_time = timezone.now()
            sync_attempt.save()
        raise  # Re-raise the exception so Celery knows the task failed