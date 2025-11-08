import os
import time
import requests

LOG_PATH = os.getenv("LOG_PATH", "/var/log/nginx/access.log")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ERROR_RATE_THRESHOLD = int(os.getenv("ERROR_RATE_THRESHOLD", 2))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", 300))

last_alert = 0

def send_alert(message):
    global last_alert
    now = time.time()
    if now - last_alert < ALERT_COOLDOWN_SEC:
        return
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"[ERROR] Failed to send Slack alert: {e}")
    last_alert = now

def tail_log(path):
    try:
        with open(path, "r") as f:
            # seek end only if file is seekable
            try:
                f.seek(0, os.SEEK_END)
            except (OSError, IOError):
                pass
            while True:
                line = f.readline()
                if line:
                    yield line
                else:
                    time.sleep(0.1)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {path}")
        while True:
            time.sleep(1)

def monitor():
    window = []
    for line in tail_log(LOG_PATH):
        status = None
        parts = line.split()
        if len(parts) > 8:
            status = parts[8]
        if status and status.startswith("5"):
            window.append(1)
        else:
            window.append(0)
        if len(window) > WINDOW_SIZE:
            window.pop(0)
        if sum(window) >= ERROR_RATE_THRESHOLD:
            send_alert(f"[ALERT] High error rate detected! Last {WINDOW_SIZE} requests have {sum(window)} errors.")

if __name__ == "__main__":
    print("============================================================")
    print("[INFO] 🚀 Starting Alert Watcher...")
    print(f"[INFO] LOG_PATH: {LOG_PATH}")
    print(f"[INFO] ERROR_RATE_THRESHOLD: {ERROR_RATE_THRESHOLD}")
    print(f"[INFO] WINDOW_SIZE: {WINDOW_SIZE}")
    print(f"[INFO] ALERT_COOLDOWN_SEC: {ALERT_COOLDOWN_SEC}")
    print(f"[INFO] ✅ Found log file at {LOG_PATH}")
    print("[INFO] 👀 Monitoring Nginx log for errors...")
    monitor()
