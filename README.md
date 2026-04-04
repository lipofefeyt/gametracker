# 🎮 gametracker

A lightweight, automated Python tool to track the prices of wanted video games across various online storefronts, log their historical data, and alert you when a deal hits your personal acceptable threshold.

## 🚀 Features (Current & Planned)
- [x] Scrape prices from Steam's internal API.
- [x] Store historical pricing data in a local SQLite database.
- [ ] Send instant notifications (Telegram/Discord) when a game drops below a target price.
- [ ] Support additional storefronts (GOG, Epic, CheapShark API).
- [ ] Generate visualizations of price trends over time.
- [ ] Fully automated via GitHub Actions or Cron.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Database:** SQLite3
* **Libraries:** `requests`

## 📦 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/gametracker.git](https://github.com/YOUR_USERNAME/gametracker.git)
   cd gametracker