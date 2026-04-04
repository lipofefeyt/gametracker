import requests

# CheapShark's internal Store IDs
STORE_IDS = {
    "gog": "7",
    "humble": "11",
    "fanatical": "15"
}

def get_price(steam_app_id, store_name):
    """Fetches the price from CheapShark for a specific store using the Steam ID."""
    # We search CheapShark using the Steam ID
    url = f"https://www.cheapshark.com/api/1.0/games?steamAppID={steam_app_id}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data:
            return None # Game not found on CheapShark
            
        # CheapShark returns a list, usually with 1 exact match for a Steam ID
        game_info = data[0]
        deals = game_info.get("deals", [])
        
        target_store_id = STORE_IDS.get(store_name.lower())
        
        # Loop through the deals to find the specific store we want
        for deal in deals:
            if deal["storeID"] == target_store_id:
                return float(deal["price"])
                
    except Exception as e:
        print(f"Error fetching from CheapShark: {e}")
        
    return None