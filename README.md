# 🎮 GameTracker

A fully automated, cloud-hosted Python tool that tracks video game prices across multiple digital storefronts. It runs daily via GitHub Actions, logs historical pricing data to SQLite, and emails you when a game drops below your personal target price.

## 🚀 Supported Storefronts
Thanks to a modular plugin architecture and the **CheapShark API**, GameTracker currently supports:
- ✅ **Steam** (Native API)
- ✅ **GOG** (via CheapShark)
- ✅ **Fanatical** (via CheapShark)
- ✅ **Humble Bundle** (via CheapShark)
- ✅ **Nintendo Switch** (via Deku Deals)

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.10
* **Database:** SQLite3 (Normalized schema with cross-store support)
* **CI/CD:** GitHub Actions (Automated Daily Cron Job)
* **Notifications:** Native SMTP Email integration

### Folder Structure
The codebase uses a scalable `src/` pattern to easily drop in new store plugins:
```text
gametracker/
├── .github/workflows/   # Cloud Automation
├── data/
│   └── tracker.db       # SQLite Database (gitignored)
├── docs/
│   └── index.html       # GitHub Pages dashboard (auto-generated)
├── src/
│   ├── scrapers/        # Storefront Plugins
│   │   ├── steam.py
│   │   ├── cheapshark.py
│   │   └── nintendo.py  # Deku Deals scraper for Switch titles
│   ├── db_manager.py
│   ├── notify.py
│   └── visualize.py     # Plotly dashboard generator
├── add_game.py          # Interactive CLI Tool
└── main.py              # Master Routing Loop