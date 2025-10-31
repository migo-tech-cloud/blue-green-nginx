
---

### **runbook.md**

```markdown
# Blue-Green Deployment Runbook

This runbook describes steps to deploy, maintain, and troubleshoot the Blue-Green Nginx project with alert watcher.

---

## 1️⃣ Deploying the Project

1. Clone repository and navigate to `stage3/`:

```bash
git clone https://github.com/<your-org>/blue-green-nginx.git
cd blue-green-nginx/stage3
Set environment variables:

bash
Copy code
cp .env.example .env
nano .env
Build and start containers:

bash
Copy code
sudo docker compose up --build -d
Verify container status:

bash
Copy code
sudo docker ps
2️⃣ Triggering Blue-Green Failures for Testing
Add a temporary Nginx config snippet for 500 errors:

bash
Copy code
echo 'location /500 { return 500; }' | sudo tee /home/ubuntu/blue-green-nginx/stage3/nginx_conf_500.conf
sudo docker cp /home/ubuntu/blue-green-nginx/stage3/nginx_conf_500.conf nginx_proxy:/etc/nginx/conf.d/
sudo docker exec nginx_proxy nginx -s reload
Generate errors:

bash
Copy code
for i in {1..10}; do curl -I http://localhost/500; done
Watch alerts:

bash
Copy code
sudo docker logs -f alert_watcher
3️⃣ Stopping / Cleaning Up
bash
Copy code
sudo docker compose down -v
sudo docker system prune -f
The -v removes associated volumes to avoid stale log files.

Use sudo docker volume ls to inspect volumes.

4️⃣ Troubleshooting
Watcher shows blank logs:

Ensure /var/log/nginx/access.log is a real file (not symlink to /dev/stdout).

Remove old log volumes: sudo docker volume rm stage3_nginx_logs

Recreate containers: sudo docker compose up -d --build

Slack alerts not firing:

Check SLACK_WEBHOOK_URL in .env

Check watcher logs: sudo docker logs -f alert_watcher

Nginx reload issues:

Edit nginx.conf.template or add /etc/nginx/conf.d/*.conf

Reload with sudo docker exec nginx_proxy nginx -s reload

5️⃣ Verification
Ensure app endpoints are working:

bash
Copy code
curl -I http://localhost/version
curl -I http://localhost/t/
Check watcher detects errors and posts to Slack.

All alerts should include:

pool, release_id, status code, request_time, etc.

6️⃣ Maintenance
Rotate logs or truncate to avoid huge files:

bash
Copy code
sudo truncate -s 0 logs/access.log
sudo truncate -s 0 logs/error.log
Keep .env secure.

Update Docker images periodically.
