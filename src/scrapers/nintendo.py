import requests
from bs4 import BeautifulSoup
import re

def get_price(url):
    """Scrapes the raw HTML of a Nintendo eShop page to find the price."""
    
    # Websites block scripts. We MUST use a User-Agent to pretend to be a real browser.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Throw an error if the page is a 404
        
        # Parse the chaotic HTML into a beautiful, searchable tree
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # PRO TIP: Website layouts change constantly. 
        # We look for the € symbol next to numbers anywhere in the main content.
        # This is often more reliable than guessing the exact CSS class Nintendo uses today.
        
        # Example: Find all text containing something like "59,99 €" or "€19.99"
        text_blocks = soup.find_all(string=re.compile(r'[0-9]+[,.][0-9]+\s*€|€\s*[0-9]+[,.][0-9]+'))
        
        if text_blocks:
            # Grab the first match (usually the main price)
            raw_price = text_blocks[0]
            
            # Clean it up: Remove the €, replace commas with dots, and turn it into a float
            clean_price = re.sub(r'[^\d,.]', '', raw_price).replace(',', '.')
            return float(clean_price)
            
        print(f"⚠️ Could not find a Euro price on: {url}")
        return None
        
    except Exception as e:
        print(f"Error scraping Nintendo eShop: {e}")
        return None

# Quick local test
if __name__ == "__main__":
    # Test with a real EU Nintendo URL
    test_url = "https://www.nintendo.fr/Jeux/Jeux-Nintendo-Switch/The-Legend-of-Zelda-Tears-of-the-Kingdom-2270788.html"
    print(f"Current price: {get_price(test_url)}€")