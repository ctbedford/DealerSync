from celery import shared_task
from .scraper import run_all_scrapers
from .models import SyncAttempt, VehicleListing
from django.contrib.auth import get_user_model
from django.utils import timezone
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

logger = get_task_logger(__name__)


@shared_task(bind=True)
def run_scrapers(self, user_id):
    channel_layer = get_channel_layer()
    User = get_user_model()
    sync_attempt = None

    def update_progress(current, total, current_vehicle):
        progress = int((current / total) * 100) if total > 0 else 0
        message = {
            'user_id': user_id,
            'current': current,
            'total': total,
            'percent': progress,
            'currentVehicle': current_vehicle
        }
        self.update_state(state='PROGRESS', meta=message)
        try:
            async_to_sync(channel_layer.group_send)(
                f'sync_{user_id}',
                {
                    'type': 'sync_message',
                    'message': json.dumps(message)
                }
            )
            logger.info(f"WebSocket message sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send WebSocket message: {str(e)}")
        logger.info(f"Updated task state: {
                    progress}% complete, current vehicle: {current_vehicle}")

    try:
        user = User.objects.get(id=user_id)
        sync_attempt = SyncAttempt.objects.create(
            user=user,
            status='IN_PROGRESS',
            task_id=self.request.id
        )

        update_progress(0, 100, 'Starting scrape...')
        logger.info(f"Starting scrape for user {user_id}")

        listings = run_all_scrapers(user_id) or []
        logger.info(f"Scraped {len(listings)} listings")

        if not listings:
            logger.warning("No listings returned from scraper")
            sync_attempt.status = 'COMPLETED'
            sync_attempt.end_time = timezone.now()
            sync_attempt.save()
            update_progress(100, 100, 'No listings found')
            return "No listings found"

        listings_added = 0
        listings_updated = 0
        total_listings = len(listings)

        for index, listing_data in enumerate(listings, start=1):
            unique_identifier = listing_data.get('unique_identifier')
            if not unique_identifier:
                logger.warning(
                    f"Skipping listing without unique identifier: {listing_data}")
                continue

            current_vehicle = f"{listing_data.get(
                'year', 'N/A')} {listing_data.get('make', 'N/A')} {listing_data.get('model', 'N/A')}"

            try:
                listing, created = VehicleListing.objects.update_or_create(
                    user=user,
                    unique_identifier=unique_identifier,
                    defaults={
                        'dealership': listing_data.get('dealership'),
                        'title': listing_data.get('title'),
                        'price': listing_data.get('price'),
                        'msrp': listing_data.get('msrp'),
                        'year': listing_data.get('year'),
                        'make': listing_data.get('make'),
                        'model': listing_data.get('model'),
                        'image_url': listing_data.get('image_url'),
                        'needs_update': False
                    }
                )

                if created:
                    listings_added += 1
                else:
                    listings_updated += 1

                update_progress(index, total_listings, current_vehicle)
            except Exception as e:
                logger.error(f"Error processing listing {
                             unique_identifier}: {str(e)}")

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
        update_progress(total_listings, total_listings, 'Scraping completed')
        return f"Scraping completed successfully. Added: {listings_added}, Updated: {listings_updated}"

    except Exception as e:
        logger.error(f"Error in run_scrapers task: {str(e)}")
        if sync_attempt:
            sync_attempt.status = 'FAILED'
            sync_attempt.error_message = str(e)
            sync_attempt.end_time = timezone.now()
            sync_attempt.save()
        update_progress(0, 100, f'Error: {str(e)}')
        raise
