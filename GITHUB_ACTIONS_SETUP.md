# GitHub Actions Setup Guide - Step by Step

## 🎯 **Quick Setup (10 minutes)**

Follow these exact steps to set up automated deployment on GitHub Actions:

---

## **STEP 1: Add Telegram Secrets** (2 minutes)

### Go to Repository Settings:
1. Open: https://github.com/dhinetrya-jpg/stock_live_announcement_bot
2. Click: **Settings** (top navigation)
3. Left sidebar: Click **Secrets and variables** → **Actions**

### Add Secret #1: TELEGRAM_TOKEN
1. Click **New repository secret**
2. **Name:** `TELEGRAM_TOKEN`
3. **Value:** `8820633468:AAGXkX-LS_gfFikqP7tZNOwc9fy5nkRTrMY`
4. Click **Add secret**

### Add Secret #2: TELEGRAM_CHAT_ID
1. Click **New repository secret**
2. **Name:** `TELEGRAM_CHAT_ID`
3. **Value:** `-1003748866784`
4. Click **Add secret**

**Expected:**
```
✅ TELEGRAM_TOKEN (added 1 second ago)
✅ TELEGRAM_CHAT_ID (added just now)
```

---

## **STEP 2: Create Workflow File** (3 minutes)

The workflow file `.github/workflows/nse-tracker.yml` is already created in your repository!

### Verify it exists:
1. Go to: https://github.com/dhinetrya-jpg/stock_live_announcement_bot
2. Navigate to: **.github/workflows/nse-tracker.yml**
3. You should see the complete workflow configuration ✅

---

## **STEP 3: Verify Setup** (2 minutes)

### Check Secrets are Added:
1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Verify:
   - ✅ TELEGRAM_TOKEN
   - ✅ TELEGRAM_CHAT_ID

### Check Workflow File:
1. Navigate to: **.github/workflows/nse-tracker.yml**
2. Verify the file contains the workflow configuration

---

## **STEP 4: Test the Workflow** (2-3 minutes)

### Manual Trigger Test:
1. Go to: **Actions** tab → https://github.com/dhinetrya-jpg/stock_live_announcement_bot/actions
2. Left sidebar: Click **NSE Tracker - Production Deployment**
3. Click **Run workflow** button (right side)
4. Select branch: **main** (default)
5. Click **Run workflow** button

### Wait for Execution:
```
Status will show as: 🟡 Running (1-3 minutes)
Then: ✅ Success
```

### View Execution Details:
1. Click on the workflow run
2. Click on **nse-tracker-job**
3. Expand each step to see output:
   - ✅ Checkout repository code
   - ✅ Set up Python 3.9
   - ✅ Install Python dependencies
   - ✅ Run validation tests
   - ✅ Run NSE Tracker
   - ✅ Upload tracker logs as artifact

**Expected Output:**
```
✅ Running validation tests...
✅ Tests completed
🚀 Starting NSE Tracker...
✅ Tracker completed
✅ NSE Tracker workflow completed successfully
📊 Logs available in artifacts
```

---

## **STEP 5: Download Logs & Artifacts** (1 minute)

### After Successful Run:
1. Go to workflow run details
2. Scroll down to **Artifacts** section
3. Download:
   - 📄 `tracker-logs-X-Y.zip` - Contains tracker.log
   - 📄 `processed-ids-X.zip` - Contains processed.txt

### Extract and View:
```bash
unzip tracker-logs-1-1.zip
cat tracker.log
```

---

## 🕐 **AUTOMATIC SCHEDULE**

### Current Schedule:
```
Cron: 0 */6 * * *
Runs at: 00:00, 06:00, 12:00, 18:00 UTC
```

### In Your Timezone:
- **IST (UTC+5:30):** 5:30 AM, 11:30 AM, 5:30 PM, 11:30 PM
- **EST (UTC-5):** 7:00 PM, 1:00 AM, 7:00 AM, 1:00 PM
- **PST (UTC-8):** 4:00 PM, 10:00 PM, 4:00 AM, 10:00 AM

### Change Schedule (Optional):
Edit `.github/workflows/nse-tracker.yml`:
```yaml
schedule:
  - cron: '0 * * * *'      # Every hour
  - cron: '0 9,17 * * *'   # 9 AM & 5 PM UTC
  - cron: '*/30 * * * *'   # Every 30 minutes
```

Reference: https://crontab.guru

---

## 📊 **WORKFLOW VISUALIZATION**

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Workflow                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Trigger: Every 6 hours (0 */6 * * *) + Manual + On Push    │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 1: Checkout Code                               │   │
│  │ ✅ git clone repository                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 2: Setup Python 3.9                            │   │
│  │ ✅ python --version → 3.9.x                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 3: Install Dependencies                        │   │
│  │ ✅ pip install -r requirements.txt                  │   │
│  │ ✅ requests, urllib3 installed                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 4: Run Validation Tests                        │   │
│  │ ✅ python test_tracker.py                           │   │
│  │ ✅ 9/9 tests pass                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 5: Run NSE Tracker                             │   │
│  │ ✅ python tracker.py                                │   │
│  │ ✅ Fetch announcements from NSE                    │   │
│  │ ✅ Send Telegram alerts                            │   │
│  │ ✅ Log results to tracker.log                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Step 6: Upload Artifacts                            │   │
│  │ ✅ tracker.log (30 days retention)                 │   │
│  │ ✅ processed.txt (30 days retention)               │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│              ✅ Workflow Complete                            │
│         📱 Telegram alerts received                          │
│         📊 Logs available in artifacts                       │
│         ⏰ Next run in 6 hours                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ **SETUP VERIFICATION CHECKLIST**

- [ ] **Secrets Added:**
  - [ ] TELEGRAM_TOKEN = `8820633468:AAGXkX-LS_gfFikqP7tZNOwc9fy5nkRTrMY`
  - [ ] TELEGRAM_CHAT_ID = `-1003748866784`

- [ ] **Workflow File:**
  - [ ] File exists at `.github/workflows/nse-tracker.yml`
  - [ ] Visible in Actions tab
  - [ ] Shows "NSE Tracker - Production Deployment"

- [ ] **Manual Test:**
  - [ ] Triggered workflow manually
  - [ ] All tests passed (9/9)
  - [ ] Tracker ran successfully
  - [ ] Logs uploaded to artifacts

- [ ] **Scheduled Runs:**
  - [ ] Workflow visible in "All workflows"
  - [ ] Schedule shows: "0 */6 * * *"
  - [ ] Next run time calculated

---

## 📱 **TELEGRAM ALERTS**

### You will receive Telegram messages like:

```
🔔 NSE Corporate Announcement

📈 Stock: RELIANCE
📅 Date: 2026-05-20
📌 Subject: Board Approval for Stock Split
📝 Details: Board approved 1:5 stock split
🔗 [View Document]
```

### Notifications sent to:
- **Chat ID:** -1003748866784
- **Frequency:** Every 6 hours (or whenever new announcements found)
- **Automated:** Yes (no manual action needed)

---

## 🔧 **TROUBLESHOOTING**

### **Secrets not visible in workflow:**
- Go to: Settings → Secrets and variables → Actions
- Verify exact names (case-sensitive):
  - `TELEGRAM_TOKEN` (not token)
  - `TELEGRAM_CHAT_ID` (not chat_id)
- Ensure no extra spaces in values

### **Workflow doesn't appear in Actions tab:**
- Wait 30-60 seconds and refresh page
- Check file is exactly at: `.github/workflows/nse-tracker.yml`
- Check for YAML syntax errors

### **Manual test fails:**
- Check secrets are set correctly
- Check internet connectivity
- Verify NSE website is accessible (test manually)
- View full error logs in workflow run

### **Cron schedule not working:**
- GitHub Actions uses UTC timezone
- Schedule `0 */6 * * *` = 00:00, 06:00, 12:00, 18:00 UTC
- Wait for next scheduled time (may take up to 15 mins)
- Manual trigger works = cron scheduler is OK

### **Alerts not received on Telegram:**
- Verify chat ID is correct (should be negative for groups)
- Check bot is added to group
- View workflow logs for Telegram API errors
- Test manually: `curl https://api.telegram.org/bot<token>/sendMessage`

---

## 🎯 **NEXT ACTIONS**

1. ✅ **Add Secrets:**
   - Go to Settings → Secrets
   - Add TELEGRAM_TOKEN and TELEGRAM_CHAT_ID

2. ✅ **Verify Workflow:**
   - Go to Actions tab
   - Confirm workflow file is there

3. ✅ **Test Manually:**
   - Run workflow → Run workflow button
   - Wait for execution
   - Check logs and artifacts

4. ✅ **Monitor Runs:**
   - Check Actions tab regularly
   - View logs and download artifacts
   - Verify Telegram messages received

5. ✅ **Done!**
   - Workflow is now automated
   - Runs every 6 hours automatically
   - Alerts sent to Telegram group

---

## 📈 **MONITORING DASHBOARD**

### Check Status Anytime:
**URL:** https://github.com/dhinetrya-jpg/stock_live_announcement_bot/actions

Shows:
- ✅ All workflow runs
- ✅ Status (Success/Failed/Running)
- ✅ Execution time
- ✅ Artifacts available
- ✅ Last run details

---

## 🚀 **YOU'RE ALL SET!**

Your NSE Tracker is now:
- ✅ Running automatically every 6 hours
- ✅ Sending Telegram alerts
- ✅ Storing logs for 30 days
- ✅ Fully monitored and logged

**No manual intervention needed!** 📱✅

Telegram messages will arrive automatically. Monitor the Actions tab anytime to view detailed logs.

