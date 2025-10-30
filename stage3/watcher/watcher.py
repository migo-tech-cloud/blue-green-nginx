import os
import time
import json
import requests
from collections import deque

# --- Load Environment Variables ---
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ACTIVE_POOL = os.getenv("ACTIVE_POOL", "blue")
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 2))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", 300))
LOG_PATH = "/var/log/nginx/access.log"

# --- Internal State ---
last_pool = ACTIVE_POOL
last_alert_time = 0
error_window = deque(maxlen=WINDOW_SIZE)

def send_slack_alert(message, alert_type="info"):
    """Send formatted message to Slack"""
    global last_alert_time
    now = time.time()

    # Respect cooldown
    if now - last_alert_time < ALERT_COOLDOWN_SEC:
        return

    payload = {
        "text": f":rotating_light: *{alert_type.upper()} ALERT*\n{message}"
    }

    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        last_alert_time = now
        print(f"[INFO] Alert sent to Slack: {message}")
    except Exception as e:
        print(f"[ERROR] Failed to send Slack alert: {e}")

def analyze_log_line(line):
    """Parse Nginx access log line"""
    global last_pool

    # Expect log format fields like:
    # pool=blue release=blue-v1 upstream_status=200 ...
    parts = line.strip().split()
    data = {}
    for part in parts:
        if '=' in part:
            key, val = part.split('=', 1)
            data[key] = val

    pool = data.get("pool")
    upstream_status = data.get("upstream_status", "")
    status_code = upstream_status if upstream_status.isdigit() else "0"

    # Detect pool flip
    if pool and pool != last_pool:
        send_slack_alert(
            f"Failover detected! Pool switched from *{last_pool}* → *{pool}*.",
            alert_type="failover"
        )
        last_pool = pool

    # Track 5xx errors
    if status_code.startswith("5"):
        error_window.append(1)
    else:
        error_window.append(0)

    if len(error_window) == WINDOW_SIZE:
        error_rate = sum(error_window) / WINDOW_SIZE * 100
        if error_rate > ERROR_RATE_THRESHOLD:
            send_slack_alert(
                f"High error rate detected: {error_rate:.2f}% 5xx responses in last {WINDOW_SIZE} requests.",
                alert_type="error-rate"
            )

def tail_log(file_path):
    """Continuously read log file"""
    print("[INFO] Starting log watcher...")
    with open(file_path, "r") as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if line:
                analyze_log_line(line)
            else:
                time.sleep(0.5)

if __name__ == "__main__":
    if not SLACK_WEBHOOK_URL:
        print("[ERROR] SLACK_WEBHOOK_URL not set. Exiting.")
        exit(1)
    try:
        tail_log(LOG_PATH)
    except KeyboardInterrupt:
        print("\n[INFO] Watcher stopped manually.")
