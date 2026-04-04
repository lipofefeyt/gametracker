import requests

def get_price(app_id):
    """Fetches the current price from the Steam API in EUR."""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=fr"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data[app_id]["success"]:
            game_data = data[app_id]["data"]
            price_info = game_data.get("price_overview")
            
            if price_info:
                return price_info["final"] / 100
            else:
                return 0.0 # Free game
    except Exception as e:
        print(f"Error fetching Steam ID {app_id}: {e}")
    
    return None