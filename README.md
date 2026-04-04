# 🎮 Game Price Tracker

A fully automated, cloud-hosted Python tool that tracks video game prices on Steam. It runs daily via GitHub Actions, logs historical pricing data to SQLite, and emails you when a game drops below your personal target price.

## 🚀 Features
- **Cloud Automation:** Runs automatically every day at 10:00 AM UTC using GitHub Actions.
- **SQLite Storage:** Keeps a historical ledger of prices to track sales trends.
- **Email Alerts:** Automatically fires an email to your inbox when a deal is found.
- **Localized Pricing:** Configured to pull EU pricing (€) directly from the Steam API.

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Database:** SQLite3
* **CI/CD:** GitHub Actions
* **Libraries:** `requests`, `python-dotenv`

## ➕ How to Track a New Game

Because the database lives on GitHub and is updated daily by the server, follow this workflow to add new games:

1. **Pull the latest database from the cloud:**
   ```bash
   git pull origin main