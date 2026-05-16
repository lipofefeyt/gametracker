import src.db_manager as db
import src.notify as notify
import src.visualize as visualize
from src.scrapers import steam, cheapshark, nintendo

SCRAPER_MAP = {
    "steam": steam.get_price,
    "gog": lambda app_id: cheapshark.get_price(app_id, "gog"),
    "fanatical": lambda app_id: cheapshark.get_price(app_id, "fanatical"),
    "humble": lambda app_id: cheapshark.get_price(app_id, "humble"),
    "nintendo": nintendo.get_price,
}

def run_tracker():
    print("🚀 Starting Modular GameTracker...")
    db.setup_database()

    games = db.get_games()

    for app_id, name, target_price, store in games:
        print(f"Checking {name} on {store.upper()}...")

        if store in SCRAPER_MAP:
            current_price = SCRAPER_MAP[store](app_id)

            if current_price is not None:
                db.log_price(app_id, current_price)

                if current_price <= target_price:
                    print(f"🔥 DEAL ALERT: {name} is {current_price}€! (Target: {target_price}€)")
                    notify.send_email_alert(name, current_price, target_price)
                else:
                    print(f"   Status: Too expensive ({current_price}€).")
        else:
            print(f"⚠️ Warning: No scraper built for '{store}'!")

    visualize.generate_dashboard()

if __name__ == "__main__":
    run_tracker()
