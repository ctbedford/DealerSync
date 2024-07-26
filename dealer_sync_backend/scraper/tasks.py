from celery import shared_task
from .scraper import run_all_scrapers
from .models import SyncAttempt, VehicleListing
from django.contrib.auth import get_user_model
from django.utils import timezone
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True)
def run_scrapers(self, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        sync_attempt = SyncAttempt.objects.create(
            user=user,
            status='IN_PROGRESS',
            task_id=self.request.id
        )
        self.update_state(state='PROGRESS', meta={
            'user_id': user_id,
            'current': 0,
            'total': 100,
            'percent': 0,
            'currentVehicle': 'Starting scrape...'
        })
        logger.info(f"Starting scrape for user {user_id}")
        listings = run_all_scrapers(user_id)
        if listings is None:
            logger.warning(
                "Scraper returned None instead of a list of listings")
            listings = []
        logger.info(f"Scraped {len(listings)} listings")
        if not listings:
            logger.warning("No listings returned from scraper")
            sync_attempt.status = 'COMPLETED'
            sync_attempt.end_time = timezone.now()
            sync_attempt.save()
            return "No listings found"
        listings_added = 0
        listings_updated = 0
        total_listings = len(listings)
        for index, listing_data in enumerate(listings, start=1):
            unique_identifier = listing_data['unique_identifier']
            current_vehicle = f"{listing_data['year']} {
                listing_data['make']} {listing_data['model']}"
            logger.info(f"Processing vehicle {
                        index}/{total_listings}: {current_vehicle}")
            listing, created = VehicleListing.objects.update_or_create(
                user=user,
                unique_identifier=unique_identifier,
                defaults={
                    'dealership': listing_data['dealership'],
                    'title': listing_data['title'],
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
            progress = int((index / total_listings) * 100)
            self.update_state(state='PROGRESS', meta={
                'user_id': user_id,
                'current': index,
                'total': total_listings,
                'percent': progress,
                'currentVehicle': current_vehicle
            })
            logger.info(f"Updated task state: {
                        progress}% complete, current vehicle: {current_vehicle}")
        # Mark listings that weren't updated as needing update
        VehicleListing.objects.filter(
            user=user,
            updated_at__lt=timezone.now() - timezone.timedelta(hours=1)
        ).update(needs_update=True)
        sync_attempt.status = 'COMPLETED'
        sync_attempt.listings_added = listings_added
        sync_attempt.listings_updated = listings_updated
        sync_attempt.end_time = timezone.now()
        sync_attempt.save()
        logger.info(f"Scraping completed. Added: {
                    listings_added}, Updated: {listings_updated}")
        return f"Scraping completed successfully. Added: {listings_added}, Updated: {listings_updated}"
    except Exception as e:
        logger.error(f"Error in run_scrapers task: {str(e)}")
        if 'sync_attempt' in locals():
            sync_attempt.status = 'FAILED'
            sync_attempt.error_message = str(e)
            sync_attempt.end_time = timezone.now()
            sync_attempt.save()
        raise
