import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

def send_email_alert(game_name, price, target_price):
    """Sends an email alert using Gmail's SMTP server."""
    if not all([SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL]):
        print("[Warning] Email credentials missing in .env file.")
        return

    # Create the email structure
    msg = EmailMessage()
    msg['Subject'] = f"🔥 Deal Alert: {game_name} is ${price:.2f}!"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    # The body of the email
    body = f"""
    🔥 DEAL ALERT 🔥
    
    🎮 Game: {game_name}
    💰 Current Price: ${price:.2f}
    🎯 Target Price: ${target_price:.2f}
    """
    msg.set_content(body)
    
    try:
        # Connect to Gmail's server securely
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[Notify] Successfully sent Email alert for {game_name}.")
    except Exception as e:
        print(f"[Notify] Error sending Email: {e}")

# Quick test if you run this file directly
if __name__ == "__main__":
    send_email_alert("Test Game", 19.99, 20.00)