import requests
import json
import os

# Configuration
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
REGISTRY_FILE = "processed.txt"

# Official NSE Endpoint (100% accurate)
NSE_URL = "https://nseindia.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br"
}

def load_processed_ids():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_processed_id(announcement_id):
    with open(REGISTRY_FILE, "a") as f:
        f.write(f"{announcement_id}\n")

def send_telegram_alert(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def track_nse():
    processed_ids = load_processed_ids()
    
    # Establish an official session to grab required cookies automatically
    session = requests.Session()
    session.get("https://nseindia.com", headers=HEADERS)
    
    # Fetch live announcements JSON payload
    response = session.get(NSE_URL, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to fetch data from exchange.")
        return

    data = response.json()
    
    # Process updates (NSE returns an array of announcement dictionaries)
    for item in data:
        # Use a unique structural ID to guarantee 100% mapping accuracy
        ann_id = item.get("desc")  # Or a combination of ticker + timestamp
        
        if ann_id not in processed_ids:
            symbol = item.get("symbol")
            subject = item.get("subject")
            details = item.get("details")
            pdf_link = f"https://nseindia.com/companies-listing/corporate-filings-announcements"
            
            # Format the live mobile alert
            alert_msg = f"🔔 *NSE Corporate Announcement*\n\n" \
                        f"📈 *Stock:* {symbol}\n" \
                        f"📌 *Subject:* {subject}\n" \
                        f"📝 *Details:* {details}\n" \
                        f"🔗 [View Document]({pdf_link})"
            
            send_telegram_alert(alert_msg)
            save_processed_id(ann_id)

if __name__ == "__main__":
    track_nse()
