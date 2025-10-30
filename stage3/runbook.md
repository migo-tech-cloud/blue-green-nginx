# Runbook – Observability & Alerts for Blue-Green Deployment

### 🚨 Failover Alert
**Message:** "Failover detected: blue → green"
**Meaning:** Nginx switched traffic from the active pool to the backup.
**Action:**
1. Run `docker ps` to confirm the failed container’s health.
2. Inspect app logs: `docker logs app_blue` or `app_green`.
3. Once stable, redeploy or restart the affected service.

---

### ⚠️ High Error Rate Alert
**Message:** "High error rate detected! X% 5xx responses"
**Meaning:** More than the allowed % of requests are failing.
**Action:**
1. Check which pool was active from logs.
2. Inspect upstream logs (`docker logs app_*`).
3. Scale up or roll back if needed.

---

### 🛠️ Recovery
**Message:** "Traffic restored to blue"
**Meaning:** System recovered; normal routing resumed.
**Action:** Monitor performance for 10–15 mins before closing alert.

---

### 💤 Maintenance Mode
If running planned updates, disable alerts by stopping watcher temporarily:
```bash
docker stop alert_watcher
