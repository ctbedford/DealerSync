from celery import shared_task
from .scraper import run_all_scrapers
from celery.utils.log import get_task_logger
from .models import SyncAttempt, VehicleListing
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()
logger = get_task_logger(__name__)

@shared_task
def run_scrapers(user_id):
    user = User.objects.get(id=user_id)
    sync_attempt = SyncAttempt.objects.create(status='IN_PROGRESS', user=user)
    try:
        listings = run_all_scrapers()
        
        # Clear existing listings for this user
        VehicleListing.objects.filter(user=user).delete()
        
        # Add new listings
        for listing_data in listings:
            VehicleListing.objects.create(user=user, **listing_data)
        
        sync_attempt.status = 'COMPLETED'
        sync_attempt.listings_added = len(listings)
        sync_attempt.end_time = timezone.now()
        sync_attempt.save()
        
        return f"Sync completed. Added {len(listings)} listings for user {user.username}."
    except Exception as e:
        logger.error(f"Error in run_scrapers: {str(e)}")
        sync_attempt.status = 'FAILED'
        sync_attempt.error_message = str(e)
        sync_attempt.end_time = timezone.now()
        sync_attempt.save()
        return f"Sync failed: {str(e)}"