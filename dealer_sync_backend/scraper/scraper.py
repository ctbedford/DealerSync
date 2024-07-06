from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import VehicleListing
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def scrape_mclarty_daniel():
    url = "https://www.mclartydaniel.com/VehicleSearchResults?bodyType=CAR"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        # Wait for the vehicle cards to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vehicle-product-item"))
        )
        
        listings = []
        vehicle_cards = driver.find_elements(By.CLASS_NAME, "vehicle-product-item")
        
        for vehicle in vehicle_cards:
            try:
                title = vehicle.find_element(By.CLASS_NAME, "vehicle-header").text.strip()
                price = vehicle.find_element(By.CLASS_NAME, "price").text.replace('$', '').replace(',', '')
                image_url = vehicle.find_element(By.TAG_NAME, "img").get_attribute("src")
                
                listing = VehicleListing(
                    dealership="McLarty Daniel",
                    title=title,
                    price=float(price),
                    image_url=image_url,
                    # Add other fields as available
                )
                listings.append(listing)
            except Exception as e:
                logger.error(f"Error parsing vehicle: {e}")
        
        return listings
    except Exception as e:
        logger.error(f"Error fetching McLarty Daniel inventory: {e}")
        return []
    finally:
        driver.quit()


def scrape_fay_autopark():
    # Implement similar logic for Fay Autopark
    pass

def scrape_george_nunnelly():
    # Implement similar logic for George Nunnelly
    pass

def run_all_scrapers():
    all_listings = []
    all_listings.extend(scrape_mclarty_daniel())
    all_listings.extend(scrape_fay_autopark())
    all_listings.extend(scrape_george_nunnelly())
    
    # Bulk create new listings
    VehicleListing.objects.bulk_create(all_listings)
    
    # Log the scraping activity
    logger.info(f"Scraping completed at {timezone.now()}. Total listings: {len(all_listings)}")
