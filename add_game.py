import requests
import db_manager

def search_steam(query):
    """Searches the Steam storefront API and returns the top 5 matches."""
    print(f"🔍 Searching Steam for '{query}'...")
    url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=fr"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("total", 0) > 0:
            return data["items"][:5] # Return top 5 results
        else:
            return []
    except Exception as e:
        print(f"Error connecting to Steam: {e}")
        return []

def main():
    print("🎮 GAME TRACKER: ADD NEW GAME")
    print("-" * 30)
    
    search_query = input("Enter the name of the game to search: ")
    results = search_steam(search_query)
    
    if not results:
        print("❌ No games found. Try a different search term.")
        return

    # Display the results
    print("\nSelect the correct game:")
    for i, game in enumerate(results):
        print(f"[{i + 1}] {game['name']} (ID: {game['id']}) - Current Price: {game.get('price', {}).get('final', 0)/100}€")
    print("[0] Cancel")

    # Get user selection
    try:
        choice = int(input("\nEnter the number of your choice: "))
        if choice == 0 or choice > len(results):
            print("Canceled.")
            return
            
        selected_game = results[choice - 1]
        app_id = str(selected_game['id'])
        name = selected_game['name']
        
        # Get target price
        target_price = float(input(f"\nEnter your Target Price for '{name}' (e.g., 19.99): "))
        
        # Save to database
        db_manager.setup_database()
        db_manager.add_game(app_id, name, target_price)
        print(f"✅ SUCCESS: Added {name} to the database with a target of {target_price}€!")

    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    main()