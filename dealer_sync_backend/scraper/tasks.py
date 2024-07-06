from celery import shared_task
from .scraper import run_all_scrapers
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def run_scrapers():
    logger.info("Starting scraper task")
    run_all_scrapers()
    logger.info("Scraper task completed")