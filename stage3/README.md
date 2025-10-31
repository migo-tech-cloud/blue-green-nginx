# Blue-Green Deployment with Nginx and Alert Watcher

This project implements a **Blue-Green deployment setup** using Nginx as a reverse proxy and a custom Python-based **alert watcher** to monitor Nginx logs for errors and send Slack notifications.

---

## 🚀 Features

- Blue-Green deployment with **two backend app instances** (`blue_app` and `green_app`)
- **Nginx reverse proxy** with custom log formatting
- **Alert Watcher** in Python:
  - Monitors Nginx access logs
  - Sends Slack notifications when error thresholds are reached
- Configurable via `.env`
- Dockerized for easy deployment

---

## 🏗️ Project Structure

stage3/
├─ docker-compose.yml
├─ nginx.conf.template
├─ watcher/
│ ├─ Dockerfile
│ ├─ watcher.py
│ └─ requirements.txt
├─ logs/
│ ├─ access.log
│ └─ error.log
├─ .env.example
├─ README.md
└─ runbook.md


---

## ⚙️ Setup Instructions

1. **Clone the repository**:

```bash
git clone https://github.com/<your-org>/blue-green-nginx.git
cd blue-green-nginx/stage3
Create a .env file:

bash
Copy code
cp .env.example .env
nano .env
Update values as needed, e.g.:

ini
Copy code
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXX/YYYYY/ZZZZZ
ACTIVE_POOL=blue
RELEASE_ID_BLUE=v1.0
RELEASE_ID_GREEN=v2.0
ERROR_RATE_THRESHOLD=2
WINDOW_SIZE=200
ALERT_COOLDOWN_SEC=300
LOG_PATH=/var/log/nginx/access.log
Build and run containers:

bash
Copy code
sudo docker compose up --build -d
Verify containers:

bash
Copy code
sudo docker ps
Trigger test errors (optional):

bash
Copy code
for i in {1..10}; do curl -I http://localhost/500; done
Monitor alerts:

bash
Copy code
sudo docker logs -f alert_watcher
📝 Notes
The watcher monitors real Nginx logs (/var/log/nginx/access.log). Ensure real files, not symlinks (/dev/stdout), are mounted for it to work.

Slack alerts are triggered based on error rate thresholds defined in .env.

Nginx uses a custom log format with metadata for Blue-Green releases.

🛡️ Security
Do not commit your Slack webhook to the repository.

Use .env for sensitive credentials.

Follow Docker security best practices:

Remove unused volumes

Limit container privileges