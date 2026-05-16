import requests
import os

_CC = os.getenv('STEAM_COUNTRY_CODE', 'us')

def search_games(query):
    """Searches the Steam store and returns the top 5 matches."""
    url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc={_CC}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("total", 0) > 0:
            return data["items"][:5]
        return []
    except Exception as e:
        print(f"Error connecting to Steam: {e}")
        return []

def get_price(app_id):
    """Fetches the current price from the Steam API."""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc={_CC}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data[app_id]["success"]:
            price_info = data[app_id]["data"].get("price_overview")
            if price_info:
                return price_info["final"] / 100
            else:
                return 0.0  # Free game
    except Exception as e:
        print(f"Error fetching Steam ID {app_id}: {e}")

    return None
