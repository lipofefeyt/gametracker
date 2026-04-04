import requests
import db_manager

def get_steam_price(app_id):
    """Fetches the current price from the Steam API."""
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=us"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data[app_id]["success"]:
            game_data = data[app_id]["data"]
            price_info = game_data.get("price_overview")
            
            # If the game is free, price_overview might be missing
            if price_info:
                return game_data["name"], price_info["final"] / 100
            else:
                return game_data["name"], 0.0
    except Exception as e:
        print(f"Error fetching {app_id}: {e}")
    return None, None

def run_tracker():
    """Main execution loop."""
    print("Starting gametracker...")
    db_manager.setup_database()
    
    # 1. Seed some initial data (You can remove this later)
    db_manager.add_game("1245620", "Elden Ring", 40.00)
    db_manager.add_game("1086940", "Baldur's Gate 3", 30.00)

    # 2. Fetch games from DB
    db_manager.cursor.execute("SELECT app_id, name, target_price FROM games")
    games = db_manager.cursor.fetchall()

    # 3. Check prices
    for app_id, name, target_price in games:
        print(f"Checking {name}...")
        current_name, current_price = get_steam_price(app_id) 
        
        if current_price is not None:
            db_manager.log_price(app_id, current_price)
            
            if current_price <= target_price:
                print(f"🔥 DEAL ALERT: {name} is ${current_price}! (Target: ${target_price})")
            else:
                print(f"   Status: Too expensive (${current_price}).")

if __name__ == "__main__":
    run_tracker()