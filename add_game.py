import src.db_manager as db_manager
from src.scrapers import steam, nintendo

def main():
    print("🎮 GAME TRACKER: ADD NEW GAME")
    print("-" * 30)

    print("Which store do you want to track this on?")
    print("[1] Steam")
    print("[2] GOG")
    print("[3] Fanatical")
    print("[4] Humble Bundle")
    print("[5] Deku Deals (Nintendo)")

    store_choices = {"1": "steam", "2": "gog", "3": "fanatical", "4": "humble", "5": "nintendo"}
    store_choice = input("\nEnter store number (default is 1): ")
    store = store_choices.get(store_choice, "steam")

    app_id = ""
    name = ""

    if store == "nintendo":
        search_query = input(f"\nEnter the name of the game to track on Deku Deals: ")
        results = nintendo.search_games(search_query)

        if not results:
            print("❌ No games found via search.")
            print("Fallback to Manual Entry:")
            name = input("Enter the name of the game: ")
            app_id = input("Paste the full Deku Deals URL: ")
        else:
            print("\nSelect the correct game:")
            for i, game in enumerate(results):
                print(f"[{i + 1}] {game['name']}")
            print("[0] Manual URL Entry (Fallback)")

            try:
                choice = int(input("\nEnter the number of your choice: "))
                if choice == 0:
                    name = input("Enter the name of the game: ")
                    app_id = input("Paste the full URL: ")
                elif choice > len(results):
                    print("Canceled.")
                    return
                else:
                    selected_game = results[choice - 1]
                    app_id = selected_game['url']
                    name = selected_game['name']
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")
                return

    else:
        search_query = input(f"\nEnter the name of the game to track on {store.upper()}: ")
        results = steam.search_games(search_query)

        if not results:
            print("❌ No games found. Try a different search term.")
            return

        print("\nSelect the correct game:")
        for i, game in enumerate(results):
            print(f"[{i + 1}] {game['name']} (Steam ID: {game['id']})")
        print("[0] Cancel")

        try:
            choice = int(input("\nEnter the number of your choice: "))
            if choice == 0 or choice > len(results):
                print("Canceled.")
                return

            selected_game = results[choice - 1]
            app_id = str(selected_game['id'])
            name = selected_game['name']
        except ValueError:
            print("❌ Invalid input. Please enter numbers only.")
            return

    try:
        target_price = float(input(f"\nEnter your Target Price for '{name}' (e.g., 19.99): "))

        db_manager.setup_database()
        db_manager.add_game(app_id, name, target_price, store)
        print(f"✅ SUCCESS: Added {name} on {store.upper()} with a target of {target_price}€!")

    except ValueError:
        print("❌ Invalid price format. Please use numbers and a period (e.g., 19.99).")

if __name__ == "__main__":
    main()
