# NSE Stock Live Announcement Bot 📈

A Python-based bot that tracks NSE (National Stock Exchange) corporate announcements and sends real-time alerts via Telegram.

## Features ✨

- ✅ **Real-time Monitoring**: Tracks NSE announcements 24/7
- ✅ **Telegram Alerts**: Instant notifications on new announcements
- ✅ **Duplicate Prevention**: Registry system to avoid duplicate alerts
- ✅ **Error Handling**: Robust retry logic and error recovery
- ✅ **Logging**: Detailed logs for debugging and monitoring
- ✅ **Registry Cleanup**: Automatic cleanup of old entries
- ✅ **Unique ID Generation**: Composite IDs to prevent duplicates

## Prerequisites 📋

- Python 3.7 or higher
- Telegram Bot Token
- Telegram Chat ID (where alerts will be sent)

## Installation 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/dhinetrya-jpg/stock_live_announcement_bot.git
cd stock_live_announcement_bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

#### Option A: Using .env file (Recommended for local testing)
Create a `.env` file in the project root:
```bash
TELEGRAM_TOKEN=your_telegram_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

#### Option B: Export as Environment Variables
```bash
export TELEGRAM_TOKEN="your_telegram_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

#### Option C: GitHub Secrets (For GitHub Actions)
1. Go to your repository → Settings → Secrets and variables → Actions
2. Add `TELEGRAM_TOKEN` with your bot token
3. Add `TELEGRAM_CHAT_ID` with your chat ID

## Getting Telegram Credentials 🤖

### Create a Telegram Bot:
1. Open Telegram and search for `@BotFather`
2. Send `/start`
3. Send `/newbot`
4. Follow the prompts to create your bot
5. Copy the **Bot Token** (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Get Your Chat ID:
1. Open Telegram and search for `@userinfobot`
2. Send any message
3. The bot will reply with your User ID
4. For group chats, add the bot to the group and send `/start` - it will show the group ID (format: `-1001234567890`)

## Usage 💻

### Run Manually:
```bash
python tracker.py
```

### Run Tests:
```bash
python test_tracker.py
```

### Continuous Monitoring (using cron):
```bash
# Add to crontab to run every 6 hours
0 */6 * * * cd /path/to/stock_live_announcement_bot && python tracker.py
```

### Using GitHub Actions (Automated):
Create `.github/workflows/tracker.yml`:
```yaml
name: NSE Tracker

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  run-tracker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          pip install -r requirements.txt
          python tracker.py
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

## File Structure 📁

```
stock_live_announcement_bot/
├── tracker.py              # Main tracking script
├── test_tracker.py         # Validation and testing suite
├── requirements.txt        # Python dependencies
├── processed.txt           # Registry of processed announcements
├── tracker.log             # Detailed execution logs
├── VALIDATION_REPORT.md    # Code analysis and recommendations
└── README.md               # This file
```

## Configuration 🔧

### tracker.py Settings

```python
# NSE API Endpoints
NSE_API_URL = "https://www.nseindia.com/api/corporate-announcements"
NSE_HOME_URL = "https://nseindia.com"

# Registry Management
REGISTRY_FILE = "processed.txt"
MAX_REGISTRY_SIZE = 10000  # Max size before cleanup

# Log File
LOG_FILE = "tracker.log"
```

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Bot authentication token | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Target chat ID | `-1003748866784` |

## How It Works 🔄

1. **Load Registry**: Reads previously processed announcement IDs
2. **Establish Session**: Creates persistent HTTP session with NSE
3. **Fetch Data**: Retrieves latest announcements from NSE API
4. **Validate Data**: Checks for required fields (symbol, subject)
5. **Generate IDs**: Creates unique composite IDs (symbol_date_subject)
6. **Check Duplicates**: Verifies if announcement was already processed
7. **Send Alert**: Formats and sends Telegram notification
8. **Save Record**: Stores announcement ID in registry
9. **Cleanup**: Manages registry file size

## Alert Format 📲

```
🔔 NSE Corporate Announcement

📈 Stock: SYMBOLNAME
📅 Date: 2026-05-20
📌 Subject: Important Announcement
📝 Details: Announcement details here...
🔗 [View Document](link-to-pdf)
```

## Troubleshooting 🔧

### Issue: "Invalid JSON response"
**Solution**: NSE API endpoint might have changed. Check `test_tracker.py` output for current endpoint.

### Issue: "Telegram alerts not sending"
**Solution**: Verify token and chat ID using:
```bash
python test_tracker.py
```

### Issue: "Connection timeout"
**Solution**: Script has automatic retry logic (3 attempts). Check your internet connection.

### Issue: "processed.txt file growing too large"
**Solution**: Automatic cleanup runs when file exceeds 10MB. Manual cleanup:
```bash
rm processed.txt
```

## Validation Tests ✅

Run the comprehensive test suite:
```bash
python test_tracker.py
```

Tests include:
- ✅ NSE API Connectivity
- ✅ JSON Response Parsing
- ✅ Telegram Bot Validation
- ✅ Script Structure Verification

## Logging 📝

All operations are logged to `tracker.log`:
```
[2026-05-20 10:30:45] [INFO] Starting NSE Announcement Tracker
[2026-05-20 10:30:46] [INFO] Loaded 150 processed IDs from registry
[2026-05-20 10:30:47] [INFO] Found 5 announcements
[2026-05-20 10:30:48] [INFO] New announcement found: RELIANCE - Board Approval
[2026-05-20 10:30:49] [INFO] ✅ Telegram alert sent successfully
```

## Error Handling 🛡️

The script includes:
- ✅ **Retry Logic**: Automatic retries on network failures
- ✅ **Exception Handling**: Graceful handling of errors
- ✅ **Timeout Management**: 10-15 second timeouts on requests
- ✅ **JSON Parsing**: Safe JSON parsing with error reporting
- ✅ **Input Validation**: Validates announcement data before processing

## Performance Considerations ⚡

- **API Calls**: Minimal - only fetches when run
- **Registry**: ~5KB per 1000 announcements
- **Memory**: < 50MB during execution
- **Network**: ~2-3 requests per run

## Future Enhancements 🚀

- [ ] Database storage instead of text file
- [ ] Web dashboard for monitoring
- [ ] Email alerts support
- [ ] Announcement filtering by sector/stock
- [ ] Price impact analysis
- [ ] Historical data tracking
- [ ] Multiple alert channels (SMS, Email, Discord)

## License 📄

MIT License - Feel free to use and modify

## Support 💬

For issues or questions:
1. Check the [VALIDATION_REPORT.md](VALIDATION_REPORT.md)
2. Run `python test_tracker.py` for diagnostics
3. Check `tracker.log` for error details
4. Open an issue on GitHub

## Contributing 🤝

Pull requests are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

---

**Happy Tracking! 📈🚀**
