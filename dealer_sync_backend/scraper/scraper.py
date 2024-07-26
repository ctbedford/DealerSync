import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import VehicleListing
import logging
import re
from django.db import DataError
from django.contrib.auth.models import User
from urllib.parse import urljoin
import time
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

BASE_URL = "https://www.mclartydaniel.com"
VEHICLE_SEARCH_URL = urljoin(BASE_URL, "/VehicleSearchResults")
PARAMS = {
    "configCtx": '{"webId":"motp-rml-auto-portal","locale":"en_US","version":"LIVE","page":"VehicleSearchResults","secureSiteId":null}',
    "fragmentId": "view/card/63413352-/887f-4bc8-94e5-56ab589ed678",
    "limit": 24,
    "forceOrigin": "true"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def truncate_field(value, max_length=500):
    return value[:max_length] if value else value


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def standardize_vehicle_title(title):
    parts = title.split()
    year = next((part for part in parts if part.isdigit()
                and len(part) == 4), None)
    if year:
        make_model = ' '.join(parts[parts.index(year) + 1:])
        make, *model = make_model.split(' ', 1)
        model = model[0] if model else ''
        trim = ' '.join(parts[parts.index(year) + 3:])
        standardized = f"{year} {make} {model}".strip()
        if trim:
            standardized += f" {trim}"
        return standardized, year, make, model
    return title, None, None, None


def parse_price(price_text):
    if price_text.lower() == 'contact us':
        return None
    return float(price_text.replace('$', '').replace(',', ''))


def generate_unique_identifier(year, make, model, dealership):
    return f"{year}-{make}-{model}-{dealership}".lower().replace(' ', '-')


def get_vehicle_details(detail_url):
    try:
        full_url = urljoin(BASE_URL, detail_url)
        if not is_valid_url(full_url):
            logger.error(f"Invalid URL: {full_url}")
            return None, None
        response = requests.get(full_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        vin = soup.find('span', {'data-vin': True})
        vin = vin['data-vin'] if vin else None

        color = soup.find('span', {'data-exterior-color': True})
        color = color['data-exterior-color'] if color else None

        return vin, color
    except (requests.RequestException, ValueError, AttributeError) as e:
        logger.error(f"Error processing vehicle: {type(e).__name__}: {e}")


def scrape_mclarty_daniel(user_id):
    logger.info("Starting McLarty Daniel scraper")
    offset = 0
    total_processed = 0
    total_saved = 0
    all_listings = []

# Inside the main loop in scrape_mclarty_daniel:
    # time.sleep(1)
    user = User.objects.get(id=user_id)

    while True:
        PARAMS["offset"] = offset
        PARAMS["page"] = offset // 24 + 1
        logger.info(f"Fetching page {PARAMS['page']} from {
                    VEHICLE_SEARCH_URL}")
        try:
            response = requests.get(
                VEHICLE_SEARCH_URL, params=PARAMS, headers=HEADERS)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {PARAMS['page']}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        vehicles = soup.find_all(class_="vehicle-product-item")

        if not vehicles:
            break
        logger.info(f"Found {len(vehicles)} vehicles on page {PARAMS['page']}")
        for vehicle in vehicles:
            try:
                title_element = vehicle.find(class_="title")
                if not title_element:
                    logger.warning("Title element not found, skipping vehicle")
                    continue

                original_title = clean_text(title_element.text)
                standardized_title, year, make, model = standardize_vehicle_title(
                    original_title)

                if not all([year, make, model]):
                    logger.warning(f"Couldn't parse year, make, or model from title: {
                                   original_title}")
                    continue

                price_element = vehicle.find(class_="value")
                price = parse_price(
                    price_element.text) if price_element else None

                msrp_element = vehicle.find(class_="msrp")
                msrp = parse_price(msrp_element.text.replace(
                    'MSRP', '').strip()) if msrp_element else None

                image_element = vehicle.find('img')
                image_url = image_element['src'] if image_element else ""

# Extract the dealer-specific ID from the vehicle details link
                details_link = vehicle.find('a', class_='vehicle-name')['href']
                dealer_specific_id = details_link.split('/')[-1]
                full_details_url = urljoin(
                    "https://www.mclartydaniel.com", details_link)
                vin, color = get_vehicle_details(full_details_url)

                listing_data = {
                    'user': user,
                    'dealership': truncate_field("McLarty Daniel"),
                    'title': truncate_field(standardized_title),
                    'price': price,
                    'msrp': msrp,
                    'image_url': truncate_field(image_url),
                    'year': int(year),
                    'make': make,
                    'model': model,
                    'dealer_specific_id': dealer_specific_id,
                    'vin': vin,
                    'color': color,
                    'needs_update': False
                }

                obj, created = VehicleListing.objects.update_or_create(
                    dealer_specific_id=dealer_specific_id,
                    defaults=listing_data
                )

                if created:
                    logger.info(f"New vehicle added: {standardized_title}")
                else:
                    logger.info(f"Vehicle updated: {standardized_title}")

                all_listings.append(listing_data)

                total_saved += 1
                total_processed += 1

            except Exception as e:
                logger.error(f"Error processing vehicle: {e}")
                total_processed += 1
        offset += 24

        if not vehicles:
            break

    # Mark listings that weren't updated as needing update
    VehicleListing.objects.filter(
        user=user,
        dealership="McLarty Daniel",
        updated_at__lt=timezone.now() - timezone.timedelta(hours=1)
    ).update(needs_update=True)

    logger.info(f"McLarty Daniel scraper finished. Processed: {
                total_processed}, Saved/Updated: {total_saved}")
    return all_listings


def run_all_scrapers(user_id):
    try:
        return scrape_mclarty_daniel(user_id)
    except Exception as e:
        logger.error(f"Error in run_all_scrapers: {str(e)}")
        return []
