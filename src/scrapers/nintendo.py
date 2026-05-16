import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def get_price(url):
    """Scrapes Deku Deals for the current game price."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all prices on the page (Deku Deals explicitly lists prices cleanly)
        prices = soup.find_all(string=re.compile(r'[0-9]+[,.][0-9]+\s*€|€\s*[0-9]+[,.][0-9]+|\$\s*[0-9]+[,.][0-9]+'))
        
        if prices:
            # Grab the first valid price we find
            raw_price = prices[0]
            clean_price = re.sub(r'[^\d,.]', '', raw_price).replace(',', '.')
            return float(clean_price)
            
        return None
    except Exception as e:
        print(f"Error scraping price: {e}")
        return None

def search_games(query):
    """Searches the Deku Deals database directly, avoiding Search Engine bot protection."""
    print(f"🔍 Bypassing Search Engines: Searching Deku Deals for '{query}'...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # We hit their native search page directly
    url = f"https://www.dekudeals.com/search?q={urllib.parse.quote(query)}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        
        # Find all links on the search results page
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Deku Deals game URLs always start with /items/
            if href.startswith('/items/'):
                title = a_tag.get_text(strip=True)
                
                # Filter out empty text (like image links)
                if title and len(title) > 2:
                    full_url = f"https://www.dekudeals.com{href}"
                    
                    # Prevent duplicates
                    if not any(r['url'] == full_url for r in results):
                        results.append({"name": title, "url": full_url})
                        
            # Stop once we have 5 clean results
            if len(results) >= 5:
                break
                
        return results
        
    except Exception as e:
        print(f"Error searching Deku Deals: {e}")
        return []