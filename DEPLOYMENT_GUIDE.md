# DEPLOYMENT GUIDE - NSE Stock Announcement Bot

## 🚀 **Quick Start - 3 Steps**

### **Step 1: Run Validation Tests**
```bash
export TELEGRAM_TOKEN="8820633468:AAGXkX-LS_gfFikqP7tZNOwc9fy5nkRTrMY"
export TELEGRAM_CHAT_ID="-1003748866784"

python test_tracker.py
```

**Expected Output:**
```
======================================================================
NSE ANNOUNCEMENT BOT - VALIDATION TEST SUITE
======================================================================

✅ PASS Test 1: Environment Variables
✅ PASS Test 2: Telegram Token Format
✅ PASS Test 3: Telegram Chat ID Format
✅ PASS Test 4: Telegram Bot Verification (LIVE API TEST)
   └─ Bot: Stock Bot (ID: 8820633468)
✅ PASS Test 5: NSE Connectivity
✅ PASS Test 6: NSE API Endpoint (LIVE API TEST)
   └─ Valid JSON, 47 announcements fetched
✅ PASS Test 7: Script Structure
✅ PASS Test 8: Python Dependencies
✅ PASS Test 9: Registry Operations

TEST SUMMARY
✅ Passed: 9
❌ Failed: 0

🎉 ALL TESTS PASSED!
```

---

### **Step 2: Run Tracker Script**
```bash
python tracker.py
```

**Expected Output:**
```
============================================================
🚀 Starting NSE Announcement Tracker
============================================================

[2026-05-20 10:30:45] [INFO] Loaded 0 processed IDs from registry
[2026-05-20 10:30:46] [INFO] Establishing NSE session...
[2026-05-20 10:30:46] [INFO] ✅ Established NSE session
[2026-05-20 10:30:47] [INFO] Fetching NSE announcements from API...
[2026-05-20 10:30:48] [INFO] ✅ Successfully fetched data from NSE
[2026-05-20 10:30:48] [INFO] Found 47 announcements in API response
[2026-05-20 10:30:49] [INFO] 📢 New announcement found: RELIANCE - Board Approval
[2026-05-20 10:30:50] [INFO] ✅ Telegram alert sent successfully
[2026-05-20 10:30:50] [INFO] ✅ Alert sent and recorded for: RELIANCE
[2026-05-20 10:30:51] [INFO] Tracker session completed. New alerts sent: 1
============================================================
```

---

### **Step 3: Monitor Logs**
```bash
tail -f tracker.log
```

**Log Format:**
```
[2026-05-20 10:30:45] [INFO] ============================================================
[2026-05-20 10:30:45] [INFO] 🚀 Starting NSE Announcement Tracker
[2026-05-20 10:30:45] [INFO] ============================================================
[2026-05-20 10:30:46] [INFO] Loaded 0 processed IDs from registry
[2026-05-20 10:30:47] [INFO] Establishing NSE session...
[2026-05-20 10:30:47] [INFO] ✅ Established NSE session
```

---

## 🌐 **Option A: Local/Server Deployment**

### **Setup on Linux/macOS Server:**

#### 1. Clone Repository
```bash
git clone https://github.com/dhinetrya-jpg/stock_live_announcement_bot.git
cd stock_live_announcement_bot
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Set Environment Variables
```bash
export TELEGRAM_TOKEN="8820633468:AAGXkX-LS_gfFikqP7tZNOwc9fy5nkRTrMY"
export TELEGRAM_CHAT_ID="-1003748866784"
```

#### 4. Create .env File (Alternative)
```bash
# Create .env file
cat > .env << EOF
TELEGRAM_TOKEN=8820633468:AAGXkX-LS_gfFikqP7tZNOwc9fy5nkRTrMY
TELEGRAM_CHAT_ID=-1003748866784
EOF

# Load from .env
source .env
```

#### 5. Test the Setup
```bash
python test_tracker.py
```

#### 6. Run Tracker Once
```bash
python tracker.py
```

#### 7. Schedule with Cron (Every 6 hours)
```bash
# Edit crontab
crontab -e

# Add this line:
0 */6 * * * cd /path/to/stock_live_announcement_bot && python tracker.py >> cron.log 2>&1
```

#### 8. Monitor
```bash
# Watch logs in real-time
tail -f tracker.log

# Check cron logs
tail -f cron.log
```

---

## 🔄 **Option B: GitHub Actions Deployment (Automated)**

### **Setup GitHub Actions:**

#### 1. Create Secrets in GitHub
Go to: **Settings → Secrets and variables → Actions**

Add two secrets:
- `TELEGRAM_TOKEN`: `8820633468:AAGXkX-LS_gfFikqP7tZNOwc9fy5nkRTrMY`
- `TELEGRAM_CHAT_ID`: `-1003748866784`

#### 2. Create Workflow File
Create `.github/workflows/tracker-deployment.yml`:

```yaml
name: NSE Tracker - Production Deployment

on:
  # Run on schedule (every 6 hours)
  schedule:
    - cron: '0 */6 * * *'
  
  # Allow manual trigger
  workflow_dispatch:

jobs:
  tracker-run:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run validation tests
      env:
        TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: python test_tracker.py
    
    - name: Run tracker
      env:
        TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: python tracker.py
    
    - name: Upload logs
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: tracker-logs-${{ github.run_number }}
        path: tracker.log
        retention-days: 30
```

#### 3. Trigger Workflow
- Push to main branch, OR
- Go to **Actions** → Select workflow → **Run workflow**

#### 4. View Results
- Go to **Actions** tab
- Click on workflow run
- See logs and artifacts

---

## 📊 **Deployment Comparison**

| Feature | Local/Server | GitHub Actions |
|---------|--------------|-----------------|
| Setup Time | 5 minutes | 10 minutes |
| Cost | Free (own server) | Free (GitHub) |
| Monitoring | Manual | Automatic |
| Scalability | Limited | Unlimited |
| Maintenance | Manual | Automatic |
| Logs | Local file | GitHub artifacts |
| Scheduling | Cron | GitHub Actions |

---

## ✅ **Verification Checklist**

### Local Deployment:
- [ ] Dependencies installed (`pip list | grep requests`)
- [ ] Environment variables set (`echo $TELEGRAM_TOKEN`)
- [ ] Tests pass (`python test_tracker.py`)
- [ ] Tracker runs (`python tracker.py`)
- [ ] Logs created (`ls -la tracker.log`)
- [ ] Cron scheduled (`crontab -l`)

### GitHub Actions Deployment:
- [ ] Secrets added to repository
- [ ] Workflow file created
- [ ] Workflow triggered successfully
- [ ] Tests pass in Actions
- [ ] Logs uploaded to artifacts
- [ ] Emails received for failures (optional)

---

## 🐛 **Troubleshooting**

### **Issue: Tests fail with "Module not found"**
```bash
pip install -r requirements.txt
```

### **Issue: Telegram alerts not sending**
```bash
# Check token
echo $TELEGRAM_TOKEN

# Test manually
python -c "
import os
import requests
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
url = f'https://api.telegram.org/bot{token}/getMe'
print(requests.get(url).json())
"
```

### **Issue: NSE API returns error**
- Check internet connection
- Verify NSE website is accessible
- Check logs: `tail -f tracker.log`

### **Issue: Cron not running**
```bash
# Check cron service
sudo service cron status

# View cron logs
grep CRON /var/log/syslog

# Edit crontab
crontab -e

# List all cron jobs
crontab -l
```

### **Issue: GitHub Actions failing**
- Check secrets are set correctly
- View workflow logs: Actions → Workflow → Run
- Check for API rate limits
- Verify branch is `main`

---

## 📈 **Performance Metrics**

### **Expected Performance:**
- **Execution Time:** 2-5 seconds
- **Memory Usage:** < 50MB
- **Network Calls:** 2-3 per run
- **Log File Size:** ~5KB per run
- **Registry Size:** ~100 bytes per announcement

### **Scaling:**
- 100 runs/day = ~500KB logs
- 1000 announcements = ~100KB registry
- No database needed for 1 year of data

---

## 🔒 **Security Best Practices**

1. ✅ **Never commit secrets** (use `.env` or GitHub Secrets)
2. ✅ **Validate all inputs** (already implemented)
3. ✅ **Use HTTPS only** (Telegram and NSE APIs)
4. ✅ **Set file permissions** (600 for .env)
5. ✅ **Monitor logs** for suspicious activity
6. ✅ **Rotate tokens** periodically
7. ✅ **Use strong chat IDs** (group IDs recommended)

---

## 📞 **Support & Monitoring**

### **Monitor Telegram Messages:**
- All alerts go to: `-1003748866784`
- Check Telegram group for notifications
- No manual intervention needed

### **Track Execution:**
- Local: `tail -f tracker.log`
- GitHub Actions: View artifacts after run
- Cron: `tail -f cron.log`

### **Debug Information:**
```bash
# View last 50 log lines
tail -50 tracker.log

# Search for errors
grep ERROR tracker.log

# Count processed announcements
wc -l processed.txt

# Monitor in real-time
watch -n 1 'tail -20 tracker.log'
```

---

## 🚀 **Next Steps**

1. ✅ Choose deployment option (Local or GitHub Actions)
2. ✅ Run validation tests
3. ✅ Run tracker script
4. ✅ Monitor logs
5. ✅ Schedule for production
6. ✅ Set up log rotation (optional)
7. ✅ Create alerts for failures (optional)

---

**🎉 Your bot is ready for production!**

Need help? Check the README.md or VALIDATION_REPORT.md files.

