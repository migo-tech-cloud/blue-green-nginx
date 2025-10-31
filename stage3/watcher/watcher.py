import os
import time
import json
import requests
import re

# =============== CONFIGURATION ===============
LOG_PATH = os.getenv("LOG_PATH", "/var/log/nginx/access.log")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ERROR_RATE_THRESHOLD = int(os.getenv("ERROR_RATE_THRESHOLD", 2))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", 300))

last_alert_time = 0


# =============== FUNCTIONS ===============
def send_slack_alert(message):
    """Send a formatted alert to Slack"""
    if not SLACK_WEBHOOK_URL:
        print("[ERROR] SLACK_WEBHOOK_URL not set. Exiting.")
        return

    payload = {"text": f":rotating_light: *NGINX ALERT* :rotating_light:\n{message}"}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print("[INFO] Alert sent successfully to Slack.")
        else:
            print(f"[ERROR] Slack response {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to send Slack alert: {e}")


def parse_status_code(line):
    """Extract HTTP status code from NGINX log line"""
    match = re.search(r'"\s(\d{3})\s', line)
    if match:
        return int(match.group(1))
    return None


def tail_log(file_path):
    """Stream Nginx logs line-by-line safely"""
    global last_alert_time
    buffer = []

    print("[INFO] Starting log watcher...")

    try:
        with open(file_path, "r") as f:
            # Move to end of file without seeking
            for line in f:
                pass  # read until EOF to start at end

            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue

                status_code = parse_status_code(line)
                if status_code:
                    buffer.append(status_code)

                if len(buffer) > WINDOW_SIZE:
                    buffer.pop(0)

                errors = [c for c in buffer if c >= 500]
                error_rate = (len(errors) / len(buffer)) * 100 if buffer else 0

                if len(buffer) >= WINDOW_SIZE and error_rate >= ERROR_RATE_THRESHOLD:
                    now = time.time()
                    if now - last_alert_time > ALERT_COOLDOWN_SEC:
                        send_slack_alert(f"High error rate detected: {error_rate:.2f}% errors in last {WINDOW_SIZE} requests.")
                        last_alert_time = now
                    else:
                        print("[INFO] Alert suppressed due to cooldown.")
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


# =============== MAIN ENTRY ===============
if __name__ == "__main__":
    tail_log(LOG_PATH)

