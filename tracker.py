import requests
import json
import os
import logging
from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time

# Configure logging
LOG_FILE = "tracker.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
REGISTRY_FILE = "processed.txt"
MAX_REGISTRY_SIZE = 10000  # Lines before cleanup

# NSE Configuration - CORRECTED ENDPOINTS
NSE_HOME_URL = "https://nseindia.com"
NSE_API_URL = "https://www.nseindia.com/api/corporate-announcements"
today_str = datetime.now().strftime('%d-%m-%Y')

params = {
    'index': 'equities',        # <-- CRITICAL: Prevents "missing index" error
    'from_date': today_str,
    'to_date': today_str
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://nseindia.com"
}

# Request configuration
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.3


def create_session_with_retries():
    """Create a requests session with automatic retry logic"""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=MAX_RETRIES,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        backoff_factor=BACKOFF_FACTOR
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def load_processed_ids():
    """Load previously processed announcement IDs from registry"""
    try:
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "r") as f:
                ids = set(f.read().splitlines())
                logger.info(f"Loaded {len(ids)} processed IDs from registry")
                return ids
    except Exception as e:
        logger.error(f"Error loading processed IDs: {str(e)}")
    
    logger.info("Starting fresh - no processed IDs found")
    return set()


def save_processed_id(announcement_id):
    """Save announcement ID to registry file"""
    try:
        with open(REGISTRY_FILE, "a") as f:
            f.write(f"{announcement_id}\n")
        
        # Check and cleanup if file is too large
        cleanup_registry()
    except Exception as e:
        logger.error(f"Error saving processed ID: {str(e)}")


def cleanup_registry():
    """Cleanup registry file if it exceeds max size"""
    try:
        if os.path.exists(REGISTRY_FILE):
            if os.path.getsize(REGISTRY_FILE) > MAX_REGISTRY_SIZE * 100:  # Rough estimate
                with open(REGISTRY_FILE, "r") as f:
                    lines = f.readlines()
                
                # Keep last 5000 entries
                if len(lines) > 5000:
                    with open(REGISTRY_FILE, "w") as f:
                        f.writelines(lines[-5000:])
                    logger.info(f"Registry cleanup: Kept last 5000 entries")
    except Exception as e:
        logger.warning(f"Registry cleanup error: {str(e)}")


def send_telegram_alert(message):
    """Send alert message to Telegram - CORRECTED ENDPOINT"""
    try:
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            logger.error("Telegram credentials not configured in environment")
            return False
        
        # FIXED: Correct Telegram API endpoint
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        session = requests.Session()
        response = session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                logger.info("✅ Telegram alert sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {data.get('description', 'Unknown error')}")
                return False
        else:
            logger.error(f"Telegram request failed: {response.status_code}")
            return False
    
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {str(e)}")
        return False


def validate_announcement(item):
    """Validate that announcement has required fields"""
    required_fields = ["symbol", "subject"]
    
    for field in required_fields:
        if not item.get(field):
            return False
    
    return True


def generate_unique_id(item):
    """Generate composite unique ID to prevent duplicates"""
    try:
        symbol = item.get("symbol", "UNKNOWN")
        
        # Try to get date from various possible fields
        date = item.get("date") or item.get("exDate") or item.get("ann_date") or datetime.now().strftime("%Y-%m-%d")
        
        subject = item.get("subject", "")
        
        # Create composite ID
        unique_id = f"{symbol}_{date}_{hash(subject) % 10000}"
        
        return unique_id
    except Exception as e:
        logger.warning(f"Error generating unique ID: {str(e)}")
        return None


def format_telegram_message(item):
    """Format announcement data into Telegram message"""
    try:
        symbol = item.get("symbol", "N/A")
        subject = item.get("subject", "N/A")
        details = item.get("details", "N/A")
        date = item.get("date", "N/A")
        
        # Build message
        alert_msg = f"🔔 *NSE Corporate Announcement*\n\n"
        alert_msg += f"📈 *Stock:* `{symbol}`\n"
        alert_msg += f"📅 *Date:* {date}\n"
        alert_msg += f"📌 *Subject:* {subject}\n"
        
        if details and details != "N/A":
            details_short = details[:100] + "..." if len(details) > 100 else details
            alert_msg += f"📝 *Details:* {details_short}\n"
        
        alert_msg += f"🔗 [View Document](https://nseindia.com/companies-listing/corporate-filings-announcements)"
        
        return alert_msg
    except Exception as e:
        logger.error(f"Error formatting message: {str(e)}")
        return None


def establish_nse_session(session):
    """Establish session with NSE to get required cookies"""
    try:
        logger.info("Establishing NSE session...")
        response = session.get(NSE_HOME_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            logger.info("✅ Established NSE session")
            return True
        else:
            logger.warning(f"NSE home page returned {response.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Error establishing NSE session: {str(e)}")
        return False


def fetch_nse_announcements(session):
    """Fetch live announcements from NSE API - CORRECTED ENDPOINT"""
    try:
        logger.info("Fetching NSE announcements from API...")
        
        # FIXED: Correct NSE API endpoint that returns JSON
        response = session.get(NSE_API_URL, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch announcements: HTTP {response.status_code}")
            return None
        
        # Safe JSON parsing with error handling
        try:
            data = response.json()
            logger.info(f"✅ Successfully fetched data from NSE")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from NSE: {str(e)}")
            logger.debug(f"Response content (first 500 chars): {response.text[:500]}")
            return None
    
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout while fetching NSE data (>{REQUEST_TIMEOUT}s)")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error while fetching NSE data: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error fetching NSE announcements: {str(e)}")
        return None


def process_announcements(data, processed_ids):
    """Process fetched announcements and send alerts"""
    new_alerts = 0
    
    try:
        if not isinstance(data, list):
            logger.warning(f"Unexpected data format: {type(data)}. Expected list.")
            return new_alerts
        
        logger.info(f"Found {len(data)} announcements in API response")
        
        for item in data:
            try:
                # Validate announcement has required fields
                if not validate_announcement(item):
                    logger.debug(f"Skipping invalid announcement: {item}")
                    continue
                
                # Generate unique ID
                ann_id = generate_unique_id(item)
                if not ann_id:
                    logger.debug(f"Could not generate ID for: {item.get('symbol')}")
                    continue
                
                # Check if already processed
                if ann_id in processed_ids:
                    logger.debug(f"Already processed: {ann_id}")
                    continue
                
                logger.info(f"📢 New announcement found: {item.get('symbol')} - {item.get('subject')}")
                
                # Format and send alert
                alert_msg = format_telegram_message(item)
                if alert_msg:
                    if send_telegram_alert(alert_msg):
                        save_processed_id(ann_id)
                        logger.info(f"✅ Alert sent and recorded for: {item.get('symbol')}")
                        new_alerts += 1
                        
                        # Small delay between alerts
                        time.sleep(0.5)
                    else:
                        logger.warning(f"Failed to send alert for: {item.get('symbol')}")
            
            except Exception as e:
                logger.error(f"Error processing announcement: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Error processing announcements: {str(e)}")
    
    return new_alerts


def track_nse():
    """Main function to track NSE announcements"""
    logger.info("=" * 60)
    logger.info("🚀 Starting NSE Announcement Tracker")
    logger.info("=" * 60)
    
    try:
        # Load previously processed IDs
        processed_ids = load_processed_ids()
        
        # Create session with retry logic
        session = create_session_with_retries()
        
        # Establish NSE session
        if not establish_nse_session(session):
            logger.warning("Could not establish NSE session, attempting API call anyway...")
        
        # Fetch announcements from corrected endpoint
        data = fetch_nse_announcements(session)
        
        if data is None:
            logger.error("Failed to fetch announcements. Exiting.")
            return
        
        # Process announcements
        new_alerts = process_announcements(data, processed_ids)
        
        logger.info(f"Tracker session completed. New alerts sent: {new_alerts}")
        logger.info("=" * 60)
    
    except Exception as e:
        logger.error(f"Critical error in tracker: {str(e)}")
        logger.info("=" * 60)


if __name__ == "__main__":
    track_nse()
