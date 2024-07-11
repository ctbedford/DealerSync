import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import VehicleListing
import logging
import re
from django.db import DataError

logger = logging.getLogger(__name__)

BASE_URL = "https://www.mclartydaniel.com/VehicleSearchResults"
PARAMS = {
    "configCtx": '{"webId":"motp-rml-auto-portal","locale":"en_US","version":"LIVE","page":"VehicleSearchResults","secureSiteId":null}',
    "fragmentId": "view/card/63413352-887f-4bc8-94e5-56ab589ed678",
    "limit": 24,
    "forceOrigin": "true"
}

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_year_make_model(title):
    parts = title.split()
    year = next((part for part in parts if part.isdigit() and len(part) == 4), None)
    if year:
        make_model = ' '.join(parts[parts.index(year) + 1:])
        make, *model = make_model.split(' ', 1)
        model = model[0] if model else ''
        return year, make, model
    return None, None, None

def parse_price(price_text):
    if price_text.lower() == 'contact us':
        return None
    return float(price_text.replace('$', '').replace(',', ''))

def scrape_mclarty_daniel():
    logger.info("Starting McLarty Daniel scraper")
    offset = 0
    total_processed = 0
    total_saved = 0
    all_listings = []
    
    while True:
        PARAMS["offset"] = offset
        PARAMS["page"] = offset // 24 + 1
        
        try:
            response = requests.get(BASE_URL, params=PARAMS)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {PARAMS['page']}: {e}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        vehicles = soup.find_all(class_="vehicle-product-item")
        
        if not vehicles:
            break
        
        for vehicle in vehicles:
            try:
                title_element = vehicle.find(class_="title")
                if not title_element:
                    logger.warning("Title element not found, skipping vehicle")
                    continue
                
                title = clean_text(title_element.text)
                year, make, model = extract_year_make_model(title)
                
                if not all([year, make, model]):
                    logger.warning(f"Couldn't parse year, make, or model from title: {title}")
                    continue
                
                price_element = vehicle.find(class_="value")
                price = parse_price(price_element.text) if price_element else None
                
                msrp_element = vehicle.find(class_="msrp")
                msrp = parse_price(msrp_element.text.replace('MSRP', '').strip()) if msrp_element else None
                
                image_element = vehicle.find('img')
                image_url = image_element['src'] if image_element else ""
                
                obj, created = VehicleListing.objects.update_or_create(
                    dealership="McLarty Daniel",
                    title=title,
                    defaults={
                        'price': price,
                        'msrp': msrp,
                        'image_url': image_url,
                        'year': int(year),
                        'make': make,
                        'model': model,
                        'updated_at': timezone.now()
                    }
                )
                
                if created:
                    logger.info(f"New vehicle added: {title}")
                else:
                    logger.info(f"Vehicle updated: {title}")
                    
                listing_data = {
                    'dealership': "McLarty Daniel",
                    'title': title,
                    'price': price,
                    'msrp': msrp,
                    'image_url': image_url,
                    'year': int(year),
                    'make': make,
                    'model': model,
                }
                all_listings.append(listing_data)
    
                
                total_saved += 1
                total_processed += 1
                
            except Exception as e:
                logger.error(f"Error processing vehicle: {e}")
                total_processed += 1
        
        offset += 24
        
        if not vehicles:
            break
    
    logger.info(f"McLarty Daniel scraper finished. Processed: {total_processed}, Saved/Updated: {total_saved}")
    return all_listings

def run_all_scrapers():
    try:
        scrape_mclarty_daniel()
    except Exception as e:
        logger.error(f"Error in run_all_scrapers: {str(e)}")
        return []