import src.db_manager as db
import src.notify as notify
from src.scrapers import steam

# The master routing dictionary
SCRAPER_MAP = {
    "steam": steam.get_price
}

def run_tracker():
    print("🚀 Starting Modular GameTracker...")
    db.setup_database()

    # Fetch games WITH the new store column
    db.cursor.execute("SELECT app_id, name, target_price, store FROM games")
    games = db.cursor.fetchall()

    for app_id, name, target_price, store in games:
        print(f"Checking {name} on {store.upper()}...")
        
        # The magic happens here! We look up the store in our dictionary
        if store in SCRAPER_MAP:
            scraper_function = SCRAPER_MAP[store]
            current_price = scraper_function(app_id)
            
            if current_price is not None:
                db.log_price(app_id, current_price)
                
                if current_price <= target_price:
                    print(f"🔥 DEAL ALERT: {name} is {current_price}€! (Target: {target_price}€)")
                    notify.send_email_alert(name, current_price, target_price)
                else:
                    print(f"   Status: Too expensive ({current_price}€).")
        else:
            print(f"⚠️ Warning: No scraper module built for '{store}' yet!")

if __name__ == "__main__":
    run_tracker()