# watcher.py
import os
import time
import json
import requests
from collections import deque

# ===== CONFIG =====
LOG_PATH = os.environ.get("LOG_PATH", "/var/log/nginx/access.log")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
ACTIVE_POOL = os.environ.get("ACTIVE_POOL", "blue")
ERROR_RATE_THRESHOLD = float(os.environ.get("ERROR_RATE_THRESHOLD", 2.0))  # %
WINDOW_SIZE = int(os.environ.get("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.environ.get("ALERT_COOLDOWN_SEC", 300))

if not SLACK_WEBHOOK_URL:
    print("[ERROR] SLACK_WEBHOOK_URL not set. Exiting.")
    exit(1)

# ===== STATE =====
last_pool = ACTIVE_POOL
error_window = deque(maxlen=WINDOW_SIZE)
last_alert_time = 0

# ===== FUNCTIONS =====
def post_slack(message):
    global last_alert_time
    now = time.time()
    if now - last_alert_time < ALERT_COOLDOWN_SEC:
        return
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
        print(f"[INFO] Slack alert sent: {message}")
        last_alert_time = now
    except Exception as e:
        print(f"[ERROR] Failed to send Slack alert: {e}")

def parse_log_line(line):
    """Parse a single Nginx log line for pool, status"""
    parts = line.split()
    pool = None
    status = None
    for part in parts:
        if part.startswith("pool="):
            pool = part.split("=")[1]
        if part.isdigit() and len(part) == 3:
            status = int(part)
    return pool, status

def tail_log(file_path):
    """Tail the log file continuously"""
    with open(file_path, "r") as f:
        # Go to the end of the file
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            pool, status = parse_log_line(line)
            if pool and pool != last_pool:
                post_slack(f"🚨 Failover detected: {last_pool} -> {pool}")
                global last_pool
                last_pool = pool
            if status:
                error_window.append(status)
                error_rate = sum(1 for s in error_window if 500 <= s < 600) / len(error_window) * 100
                if error_rate > ERROR_RATE_THRESHOLD:
                    post_slack(f"⚠️ High 5xx error rate detected: {error_rate:.1f}% over last {WINDOW_SIZE} requests")

# ===== MAIN =====
print("[INFO] Starting log watcher...")
try:
    tail_log(LOG_PATH)
except KeyboardInterrupt:
    print("\n[INFO] Exiting watcher")

